from django.conf.urls.defaults import patterns, url, include
from django.shortcuts import redirect

from lib.misc.urlconf_decorator import decorate

from addons.urls import ADDON_ID
from amo.decorators import write
from mkt.developers.decorators import use_apps
from webapps.urls import APP_SLUG
from . import views

PACKAGE_NAME = '(?P<package_name>[_\w]+)'


# These will all start with /addon/<addon_id>/submit/
submit_patterns = patterns('',
    url('^$', lambda r, addon_id: redirect('mkt.developers.submit.7',
                                           addon_id)),
    url('^3$', views.submit_describe, name='mkt.developers.submit.3'),
    url('^4$', views.submit_media, name='mkt.developers.submit.4'),
    url('^5$', views.submit_license, name='mkt.developers.submit.5'),
    url('^6$', views.submit_select_review, name='mkt.developers.submit.6'),
    url('^7$', views.submit_done, name='mkt.developers.submit.7'),
    url('^bump$', views.submit_bump, name='mkt.developers.submit.bump'),
)

submit_apps_patterns = patterns('',
    url('^3$', use_apps(views.submit_describe),
        name='mkt.developers.submit_apps.3'),
    url('^4$', use_apps(views.submit_media),
        name='mkt.developers.submit_apps.4'),
    url('^5$', use_apps(views.submit_done),
        name='mkt.developers.submit_apps.5'),
    url('^bump$', use_apps(views.submit_bump),
        name='mkt.developers.submit_apps.bump'),
)


def marketplace_patterns(prefix):
    return patterns('',
        url('^1$', views.marketplace_paypal,
            name='mkt.developers.%s.market.1' % prefix),
        url('^2$', views.marketplace_pricing,
            name='mkt.developers.%s.market.2' % prefix),
        url('^3$', views.marketplace_upsell,
            name='mkt.developers.%s.market.3' % prefix),
        url('^4$', views.marketplace_confirm,
            name='mkt.developers.%s.market.4' % prefix),
    )

# These will all start with /app/<app_slug>/
app_detail_patterns = patterns('',
    url('^edit$', views.edit, name='mkt.developers.apps.edit'),
    url('^edit_(?P<section>[^/]+)(?:/(?P<editable>[^/]+))?$',
        views.addons_section, name='mkt.developers.apps.section'),
    url('^ownership$', views.ownership, name='mkt.developers.apps.owner'),
    url('^enable$', views.enable, name='mkt.developers.apps.enable'),
    url('^delete$', views.delete, name='mkt.developers.apps.delete'),
    url('^disable$', views.disable, name='mkt.developers.apps.disable'),
    url('^status$', views.version_list, name='mkt.developers.apps.versions'),
    url('^payments$', views.payments, name='mkt.developers.apps.payments'),
    url('^in-app-config$', views.in_app_config,
        name='mkt.developers.apps.in_app_config'),
    url('^in-app-secret$', views.in_app_secret,
        name='mkt.developers.apps.in_app_secret'),
    url('^payments/disable$', views.disable_payments,
        name='mkt.developers.apps.payments.disable'),
    url('^payments/permission/refund$', views.acquire_refund_permission,
        name='mkt.developers.apps.acquire_refund_permission'),
    url('^payments/', include(marketplace_patterns('apps'))),
    url('^profile$', views.profile, name='mkt.developers.apps.profile'),
    url('^profile/remove$', views.remove_profile,
        name='mkt.developers.apps.profile.remove'),
    url('^issue_refund$', views.issue_refund,
        name='mkt.developers.apps.issue_refund'),
    url('^refunds$', views.refunds, name='mkt.developers.apps.refunds'),
)

# These will all start with /addon/<addon_id>/
detail_patterns = patterns('',
    # Redirect to the edit page from the base.
    url('^$', lambda r, addon_id: redirect('mkt.developers.addons.edit',
                                           addon_id, permanent=True)),
    url('^edit$', views.edit, name='mkt.developers.addons.edit'),
    url('^delete$', views.delete, name='mkt.developers.addons.delete'),
    url('^disable$', views.disable, name='mkt.developers.addons.disable'),
    url('^enable$', views.enable, name='mkt.developers.addons.enable'),
    url('^cancel$', views.cancel, name='mkt.developers.addons.cancel'),
    url('^ownership$', views.ownership, name='mkt.developers.addons.owner'),
    url('^admin$', views.admin, name='mkt.developers.addons.admin'),
    url('^payments$', views.payments, name='mkt.developers.addons.payments'),
    url('^payments/disable$', views.disable_payments,
        name='mkt.developers.addons.payments.disable'),
    url('^payments/permission/refund$', views.acquire_refund_permission,
        name='mkt.developers.addons.acquire_refund_permission'),
    url('^payments/', include(marketplace_patterns('addons'))),
    url('^issue_refund$', views.issue_refund,
        name='mkt.developers.addons.issue_refund'),
    url('^refunds$', views.refunds, name='mkt.developers.addons.refunds'),
    url('^profile$', views.profile, name='mkt.developers.addons.profile'),
    url('^profile/remove$', views.remove_profile,
        name='mkt.developers.addons.profile.remove'),
    url('^edit_(?P<section>[^/]+)(?:/(?P<editable>[^/]+))?$',
        views.addons_section, name='mkt.developers.addons.section'),

    url('^upload_preview$', views.upload_image, {'upload_type': 'preview'},
        name='mkt.developers.addons.upload_preview'),
    url('^upload_icon$', views.upload_image, {'upload_type': 'icon'},
        name='mkt.developers.addons.upload_icon'),
    url('^upload$', views.upload_for_addon,
        name='mkt.developers.upload_for_addon'),
    url('^upload/(?P<uuid>[^/]+)$', views.upload_detail_for_addon,
        name='mkt.developers.upload_detail_for_addon'),

    url('^versions$', views.version_list,
        name='mkt.developers.addons.versions'),
    url('^versions/delete$', views.version_delete,
        name='mkt.developers.versions.delete'),
    url('^versions/add$', views.version_add,
        name='mkt.developers.versions.add'),
    url('^versions/stats$', views.version_stats,
        name='mkt.developers.versions.stats'),
    url('^versions/(?P<version_id>\d+)$', views.version_edit,
        name='mkt.developers.versions.edit'),
    url('^versions/(?P<version_id>\d+)/add$', views.version_add_file,
        name='mkt.developers.versions.add_file'),
    url('^versions/(?P<version>[^/]+)$', views.version_bounce),

    url('^file/(?P<file_id>[^/]+)/validation$', views.file_validation,
        name='mkt.developers.file_validation'),
    url('^file/(?P<file_id>[^/]+)/validation.json$',
        views.json_file_validation,
        name='mkt.developers.json_file_validation'),

    url('^validation-result/(?P<result_id>\d+)$',
        views.bulk_compat_result,
        name='mkt.developers.bulk_compat_result'),
    url('^validation-result/(?P<result_id>\d+).json$',
        views.json_bulk_compat_result,
        name='mkt.developers.json_bulk_compat_result'),

    url('^submit/', include(submit_patterns)),
    url('^submit/resume$', views.submit_resume,
        name='mkt.developers.submit.resume'),
    url('^request-review/(?P<status>[%s])$'
        % ''.join(map(str, views.REQUEST_REVIEW)),
        views.request_review, name='mkt.developers.request-review'),
    url('^rmlocale$', views.remove_locale,
        name='mkt.developers.remove-locale'),
)

# These will all start with /ajax/addon/<addon_id>/
ajax_patterns = patterns('',
    url('^dependencies$', views.ajax_dependencies,
        name='mkt.developers.ajax.dependencies'),
    url('^image/status$', views.image_status,
        name='mkt.developers.ajax.image.status'),

    # Performance testing
    url(r'^performance/file/(?P<file_id>\d+)/start-tests.json$',
        views.file_perf_tests_start,
        name='mkt.developers.file_perf_tests_start'),
)

packager_patterns = patterns('',
    url('^$', views.package_addon, name='mkt.developers.package_addon'),
    url('^download/%s.zip$' % PACKAGE_NAME, views.package_addon_download,
        name='mkt.developers.package_addon_download'),
    url('^json/%s$' % PACKAGE_NAME, views.package_addon_json,
        name='mkt.developers.package_addon_json'),
    url('^success/%s$' % PACKAGE_NAME, views.package_addon_success,
        name='mkt.developers.package_addon_success'),
)

urlpatterns = decorate(write, patterns('',
    url('^$', views.index, name='mkt.developers.index'),

    # Redirect people who have /addons/ instead of /addon/.
    ('^addons/\d+/.*',
     lambda r: redirect(r.path.replace('addons', 'addon', 1))),

    # Add-on submission
    url('^addon/submit/$',
        lambda r: redirect('mkt.developers.submit.1', permanent=True)),
    url('^addon/submit/1$', views.submit, name='mkt.developers.submit.1'),
    url('^addon/submit/2$', views.submit_addon,
        name='mkt.developers.submit.2'),

    # Web App submission
    url('^app/submit/$',
        lambda r: redirect('mkt.developers.submit_apps.1', permanent=True)),
    url('^app/submit/1$', use_apps(views.submit),
        name='mkt.developers.submit_apps.1'),
    url('^app/submit/2$', use_apps(views.submit_addon),
        name='mkt.developers.submit_apps.2'),

    # Standalone validator:
    url('^addon/validate/?$', views.validate_addon,
        name='mkt.developers.validate_addon'),

    # Standalone compatibility checker:
    url('^addon/check-compatibility$', views.check_addon_compatibility,
        name='mkt.developers.check_addon_compatibility'),
    url(r'^addon/check-compatibility/application_versions\.json$',
        views.compat_application_versions,
        name='mkt.developers.compat_application_versions'),

    # Add-on packager
    url('^tools/package/', include(packager_patterns)),

    # Redirect to /addons/ at the base.
    url('^addon$',
        lambda r: redirect('mkt.developers.addons', permanent=True)),
    url('^addons$', views.dashboard, name='mkt.developers.addons'),
    url('^apps$', use_apps(views.dashboard), name='mkt.developers.apps'),
    url('^upload$', views.upload, name='mkt.developers.upload'),
    url('^upload/([^/]+)(?:/([^/]+))?$', views.upload_detail,
        name='mkt.developers.upload_detail'),
    url('^standalone-upload$', views.standalone_upload,
        name='mkt.developers.standalone_upload'),
    url('^standalone-upload/([^/]+)$', views.standalone_upload_detail,
        name='mkt.developers.standalone_upload_detail'),

    url('^upload-manifest$', views.upload_manifest,
        name='mkt.developers.upload_manifest'),

    # URLs for a single add-on.
    url('^addon/%s/' % ADDON_ID, include(detail_patterns)),
    url('^app/%s/' % APP_SLUG, include(app_detail_patterns)),
    url('^app/%s/submit/' % ADDON_ID, include(submit_apps_patterns)),

    url('^ajax/addon/%s/' % ADDON_ID, include(ajax_patterns)),

    # Newsletter archive & signup
    url('community/newsletter', views.newsletter,
        name='mkt.developers.community.newsletter'),

    # Add-on SDK page
    url('builder$', views.builder, name='mkt.developers.builder'),

    # Developer docs
    url('docs/(?P<doc_name>[-_\w]+)?$',
        views.docs, name='mkt.developers.docs'),
    url('docs/(?P<doc_name>[-_\w]+)/(?P<doc_page>[-_\w]+)',
        views.docs, name='mkt.developers.docs'),

    # PayPal Checker
    url('^check_paypal$', views.check_paypal,
        name='mkt.developers.check_paypal'),
))