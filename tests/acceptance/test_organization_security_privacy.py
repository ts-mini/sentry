from __future__ import absolute_import

import time
from django.core.urlresolvers import reverse
from sentry.utils import json

from sentry.testutils import AcceptanceTestCase


class OrganizationSecurityAndPrivacyTest(AcceptanceTestCase):
    def load_organization_helper(self, snapshot_name=None):
        self.browser.wait_until_not(".loading-indicator")
        if snapshot_name is not None:
            self.browser.snapshot("organization settings security and privacy -- " + snapshot_name)
        assert self.browser.element_exists(
            '[data-test-id="organization-settings-security-and-privacy"]'
        )

    def renders_2fa_setting(self):
        return self.browser.element_exists("#require2FA")

    def test_renders_2fa_setting_for_owner(self):
        with self.feature("organizations:datascrubbers-v2"):
            user_owner = self.create_user("owner@example.com")
            organization = self.create_organization(name="Example", owner=user_owner)
            self.login_as(user_owner)
            path = "/settings/{}/security-and-privacy/".format(organization.slug)

            self.browser.get(path)
            self.load_organization_helper()
            assert self.renders_2fa_setting()

    def test_renders_2fa_setting_for_manager(self):
        with self.feature("organizations:datascrubbers-v2"):
            user_manager = self.create_user("manager@gexample.com")
            organization = self.create_organization(
                name="Example", owner=self.create_user("owner@example.com")
            )
            self.create_member(organization=organization, user=user_manager, role="manager")
            self.login_as(user_manager)
            path = "/settings/{}/security-and-privacy/".format(organization.slug)

            self.browser.get(path)
            self.load_organization_helper()
            assert self.renders_2fa_setting()

    def test_setting_2fa_without_2fa_enabled(self):
        with self.feature("organizations:datascrubbers-v2"):
            user_owner = self.create_user("owner@example.com")
            organization = self.create_organization(name="Example", owner=user_owner)
            self.login_as(user_owner)
            path = "/settings/{}/security-and-privacy/".format(organization.slug)

            self.browser.get(path)
            self.browser.wait_until_not(".loading-indicator")
            assert not self.browser.element_exists(
                '[data-test-id="organization-settings-security-and-privacy"] .error'
            )
            self.browser.click("#require2FA")

            self.browser.wait_until(".modal")
            self.browser.click('.modal [data-test-id="confirm-button"]')
            self.browser.wait_until_not(".modal")
            self.browser.wait_until_test_id("toast-error")
            self.load_organization_helper("setting 2fa without 2fa enabled")

    def test_renders_advanced_data_scrubbing_without_rule(self):
        with self.feature("organizations:datascrubbers-v2"):
            user_owner = self.create_user("owner@example.com")
            organization = self.create_organization(name="Example", owner=user_owner)
            self.login_as(user_owner)
            path = "/settings/{}/security-and-privacy/".format(organization.slug)

            self.browser.get(path)
            self.browser.wait_until_not(".loading-indicator")
            assert self.browser.element_exists('[data-test-id="advanced-data-scrubbing"]')

            self.load_organization_helper("advanced-data-scrubbing-without-rule")

    def test_renders_advanced_data_scrubbing_with_rules(self):
        with self.feature("organizations:datascrubbers-v2"):
            user_owner = self.create_user("owner@example.com")
            organization = self.create_organization(name="Example", owner=user_owner)
            relayPiiConfig = json.dumps({
                'rules': {
                    '0': {'type': 'password', 'redaction': {'method': 'replace', 'text': 'Scrubbed'}},
                    '1': {'type': 'creditcard', 'redaction': {'method': 'mask'}},
                },
                'applications': {'password': ['0'], '$message': ['1']},
            })
            organization.update_option("sentry:relay_pii_config", relayPiiConfig)
            self.login_as(user_owner)
            path = "/settings/{}/security-and-privacy/".format(organization.slug)

            self.browser.get(path)
            self.browser.wait_until_not(".loading-indicator")
            assert self.browser.element_exists('[data-test-id="advanced-data-scrubbing"]')
            assert self.browser.element_exists('[data-test-id="advanced-data-scrubbing-rules"]')
            self.load_organization_helper("advanced-data-scrubbing-with-rules")

    def test_renders_advanced_data_scrubbing_add_rule_modal(self):
        with self.feature("organizations:datascrubbers-v2"):
            user_owner = self.create_user("owner@example.com")
            organization = self.create_organization(name="Example", owner=user_owner)
            self.login_as(user_owner)
            path = "/settings/{}/security-and-privacy/".format(organization.slug)

            self.browser.get(path)
            self.browser.wait_until_not(".loading-indicator")
            assert self.browser.element_exists('[data-test-id="advanced-data-scrubbing"]')
            self.browser.click_when_visible("[aria-label='Add Rule']")
            self.load_organization_helper("advanced-data-scrubbing-add-rule-modal")
