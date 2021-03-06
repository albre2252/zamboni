(function() {
    z.page.on('fragmentloaded', function() {
        setTimeout(function() {
            // Make sure the class got updated.
            if (!$('body.reviews').length) {
                return;
            }

            initCharCount();

            // Hijack <select> with stars.
            $('select[name="rating"]').ratingwidget();

            // Handle review deletions.
            $('.delete').on('click', _pd(function() {
                var $this = $(this),
                    $r = $this.closest('.review');
                $r.addClass('deleting');
                $.post($this.attr('href')).success(function() {
                    $r.addClass('deleted');
                });
            }));

            // Toggle rating breakdown.
            var $breakdown = $('.grouped-ratings');
            $('.average-rating').on('click', _pd(function() {
                $breakdown.toggle();
            }));
            $breakdown.on('click', _pd(function() {
                $breakdown.hide();
            }));

            // "More reviews" button.
            var $more = $('.load-more');
            $more.on('click', _pd(function() {
                var $new = $('#review-list .review:visible:last ~ .review:lt(5)');
                $new.show();
                if ($new.attr('id')) {
                    // Jump to top of new reviews.
                    window.location = '#' + $new.attr('id');
                }
                // If all the reviews are visible, fetch more.
                if (!$('#review-list .review:hidden').length) {
                    // TODO: Pull in more reviews.
                    //$.get($more.attr('href'), function(data) {
                    //});
                }
            }));
        }, 0);
    });

    z.page.on('click', '.review .actions a', function(e) {
        var action = $(this).data('action');
        if (!action) return;
        e.stopPropagation();
        e.preventDefault();
        switch (action) {
            case 'edit':
                editReview($(this).closest('.review'));
            break;
            case 'report':
                flagReview($(this).closest('.review'));
            break;
        }
    });

    // review flagging. maybe make this event-driven?
    var flagOverlay = makeOrGetOverlay('flag-review'),
        currentReview,
        flagURL;

    function flagReview(reviewEl) {
        flagURL = reviewEl.data('flag-url');
        currentReview = reviewEl;
        flagOverlay.addClass('show');
    }

    flagOverlay.on('click', '.cancel', _pd(function() {
        flagOverlay.removeClass('show');
    })).on('click', '.menu a', _pd(function(e) {
        var flag = $(e.target).attr('href').slice(1),
            actionEl = currentReview.find('.actions .flag');
        flagOverlay.removeClass('show');
        actionEl.text(gettext('Sending report...'));
        $.ajax({type: 'POST',
                url: flagURL,
                data: {flag: flag},
                success: function() {
                    actionEl.replaceWith(gettext('Flagged for review'));
                },
                error: function(){ },
                dataType: 'json'
        });
    }));

    // review editing
    var editTemplate = $('#edit-review-template').html();

    function editReview(reviewEl) {
        var overlay = makeOrGetOverlay('edit-review'),
            body = reviewEl.find('.body').html(),
            rating = reviewEl.data('rating'),
            action = reviewEl.data('edit-url');
        overlay.html(format(editTemplate, {action: action, body: body}));
        overlay.find('select[name="rating"]').ratingwidget();
        overlay.find(format('.ratingwidget [value="{0}"]', rating)).click();
        overlay.addClass('show');
        overlay.find('.cancel').on('click', _pd(function() {
            overlay.removeClass('show');
        }));
    }

})();
