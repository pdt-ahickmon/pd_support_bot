import os
import time
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

# List of PagerDuty Documentation URLs
pagerduty_urls = [
    "https://support.pagerduty.com/main/docs/introduction",
    "https://support.pagerduty.com/main/docs/trial-account-onboarding",
    "https://support.pagerduty.com/main/docs/log-in-to-pagerduty",
    "https://support.pagerduty.com/main/docs/navigate-the-incidents-page",
    "https://support.pagerduty.com/main/docs/incidents",
    "https://support.pagerduty.com/main/docs/edit-incidents",
    "https://support.pagerduty.com/main/docs/reassign-incidents",
    "https://support.pagerduty.com/main/docs/incident-priority",
    "https://support.pagerduty.com/main/docs/incident-roles",
    "https://support.pagerduty.com/main/docs/incident-tasks",
    "https://support.pagerduty.com/main/docs/incident-types",
    "https://support.pagerduty.com/main/docs/custom-fields-on-incidents",
    "https://support.pagerduty.com/main/docs/why-incidents-fail-to-trigger",
    "https://support.pagerduty.com/main/docs/conference-bridge",
    "https://support.pagerduty.com/main/docs/add-responders",
    "https://support.pagerduty.com/main/docs/event-management",
    "https://support.pagerduty.com/main/docs/dynamic-notifications",
    "https://support.pagerduty.com/main/docs/communicate-with-stakeholders",
    "https://support.pagerduty.com/main/docs/status-update-templates",
    "https://support.pagerduty.com/main/docs/alerts",
    "https://support.pagerduty.com/main/docs/alerts-table",
    "https://support.pagerduty.com/main/docs/postmortems",
    "https://support.pagerduty.com/main/docs/visibility-console",
    "https://support.pagerduty.com/main/docs/notification-content-and-behavior",
    "https://support.pagerduty.com/main/docs/push-notifications",
    "https://support.pagerduty.com/main/docs/email-notifications",
    "https://support.pagerduty.com/main/docs/phone-notifications",
    "https://support.pagerduty.com/main/docs/phone-notification-disclosures",
    "https://support.pagerduty.com/main/docs/sms-notifications",
    "https://support.pagerduty.com/main/docs/sms-notification-disclosures",
    "https://support.pagerduty.com/main/docs/notification-troubleshooting",
    "https://support.pagerduty.com/main/docs/expected-notification-behavior",
    "https://support.pagerduty.com/main/docs/push-notification-troubleshooting",
    "https://support.pagerduty.com/main/docs/email-notification-troubleshooting",
    "https://support.pagerduty.com/main/docs/phone-notification-troubleshooting",
    "https://support.pagerduty.com/main/docs/sms-notification-troubleshooting",
    "https://support.pagerduty.com/main/docs/supported-countries",
    "https://support.pagerduty.com/main/docs/notification-phone-numbers",
    "https://support.pagerduty.com/main/docs/services-and-integrations",
    "https://support.pagerduty.com/main/docs/service-directory",
    "https://support.pagerduty.com/main/docs/service-profile",
    "https://support.pagerduty.com/main/docs/business-services",
    "https://support.pagerduty.com/main/docs/business-service-subscription",
    "https://support.pagerduty.com/main/docs/service-graph",
    "https://support.pagerduty.com/main/docs/maintenance-windows",
    "https://support.pagerduty.com/main/docs/email-management-filters-and-rules",
    "https://support.pagerduty.com/main/docs/regular-expressions",
    "https://support.pagerduty.com/main/docs/configurable-service-settings",
    "https://support.pagerduty.com/main/docs/integrating-with-itsm-tools",
    "https://support.pagerduty.com/main/docs/manage-users",
    "https://support.pagerduty.com/main/docs/import-users-from-a-csv",
    "https://support.pagerduty.com/main/docs/offboarding",
    "https://support.pagerduty.com/main/docs/user-roles",
    "https://support.pagerduty.com/main/docs/advanced-permissions",
    "https://support.pagerduty.com/main/docs/user-profile",
    "https://support.pagerduty.com/main/docs/teams",
    "https://support.pagerduty.com/main/docs/contextual-search",
    "https://support.pagerduty.com/main/docs/schedule-basics",
    "https://support.pagerduty.com/main/docs/edit-schedules",
    "https://support.pagerduty.com/main/docs/schedule-examples",
    "https://support.pagerduty.com/main/docs/schedules-in-apps",
    "https://support.pagerduty.com/main/docs/my-on-call-shifts",
    "https://support.pagerduty.com/main/docs/escalation-policies",
    "https://support.pagerduty.com/main/docs/round-robin-scheduling",
    "https://support.pagerduty.com/main/docs/escalation-policies-and-schedules",
    "https://support.pagerduty.com/main/docs/amazon-cloudwatch-integration-guide",
    "https://support.pagerduty.com/main/docs/amazon-eventbridge-integration-guide",
    "https://support.pagerduty.com/main/docs/aws-guardduty-integration-guide",
    "https://support.pagerduty.com/main/docs/aws-cloudtrail-integration-guide",
    "https://support.pagerduty.com/main/docs/aws-health-dashboard",
    "https://support.pagerduty.com/main/docs/aws-security-hub-integration-guide-pagerduty",
    "https://support.pagerduty.com/main/docs/bitbucket",
    "https://support.pagerduty.com/main/docs/datadog-apps-integration-guide",
    "https://support.pagerduty.com/main/docs/email-integration-guide",
    "https://support.pagerduty.com/main/docs/github-changes",
    "https://support.pagerduty.com/main/docs/gitlab-changes",
    "https://support.pagerduty.com/main/docs/jenkins-changes",
    "https://support.pagerduty.com/main/docs/jira-cloud",
    "https://support.pagerduty.com/main/docs/jira-cloud-user-guide",
    "https://support.pagerduty.com/main/docs/jira-cloud-integration-faq",
    "https://support.pagerduty.com/main/docs/jira-cloud-troubleshooting-guide",
    "https://support.pagerduty.com/main/docs/jira-server",
    "https://support.pagerduty.com/main/docs/jira-server-troubleshooting-guide",
    "https://support.pagerduty.com/main/docs/microsoft-teams",
    "https://support.pagerduty.com/main/docs/microsoft-teams-user-guide",
    "https://support.pagerduty.com/main/docs/microsoft-teams-permission-changelog",
    "https://support.pagerduty.com/main/docs/salesforce-service-cloud-integration-guide",
    "https://support.pagerduty.com/main/docs/salesforce-service-cloud-user-guide",
    "https://support.pagerduty.com/main/docs/salesforce-custom-field-mappings",
    "https://support.pagerduty.com/main/docs/servicenow-integration-guide",
    "https://support.pagerduty.com/main/docs/servicenow-integration-details",
    "https://support.pagerduty.com/main/docs/servicenow-user-guide",
    "https://support.pagerduty.com/main/docs/servicenow-provisioning",
    "https://support.pagerduty.com/main/docs/advanced-servicenow-configuration",
    "https://support.pagerduty.com/main/docs/servicenow-change-requests-integration-guide",
    "https://support.pagerduty.com/main/docs/servicenow-troubleshooting-guide",
    "https://support.pagerduty.com/main/docs/servicenow-csm-integration-guide",
    "https://support.pagerduty.com/main/docs/servicenow-csm-user-guide",
    "https://support.pagerduty.com/main/docs/slack-integration-guide",
    "https://support.pagerduty.com/main/docs/slack-permission-changelog",
    "https://support.pagerduty.com/main/docs/zendesk-integration-guide",
    "https://support.pagerduty.com/main/docs/zendesk-user-guide",
    "https://support.pagerduty.com/main/docs/zendesk-custom-field-mappings",
    "https://support.pagerduty.com/main/docs/zoom-integration-guide",
    "https://support.pagerduty.com/main/docs/nagios-troubleshooting-guide",
    "https://support.pagerduty.com/main/docs/pagerduty-agent-integration-guide",
    "https://support.pagerduty.com/main/docs/pagerduty-agent-troubleshooting-guide",
    "https://support.pagerduty.com/main/docs/solarwinds-orion-troubleshooting-guide",
    "https://support.pagerduty.com/main/docs/zabbix-troubleshooting-guide",
    "https://support.pagerduty.com/main/docs/extensions",
    "https://support.pagerduty.com/main/docs/add-ons",
    "https://support.pagerduty.com/main/docs/webhooks",
    "https://support.pagerduty.com/main/docs/custom-incident-actions",
    "https://support.pagerduty.com/main/docs/sso",
    "https://support.pagerduty.com/main/docs/live-call-routing",
    "https://support.pagerduty.com/main/docs/apps",
    "https://support.pagerduty.com/main/docs/automation-actions",
    "https://support.pagerduty.com/main/docs/pagerduty-automation-trial",
    "https://support.pagerduty.com/main/docs/incident-workflows",
    "https://support.pagerduty.com/main/docs/workflow-integrations",
    "https://support.pagerduty.com/actions/docs/incident-workflow-actions-overview",
    "https://help.catalytic.com",
    "https://docs.rundeck.com/docs/",
    "https://support.pagerduty.com/main/docs/pagerduty-advance",
    "https://support.pagerduty.com/main/docs/aiops",
    "https://support.pagerduty.com/main/docs/pagerduty-aiops-quickstart-guide",
    "https://support.pagerduty.com/main/docs/intelligent-alert-grouping",
    "https://support.pagerduty.com/main/docs/preview-intelligent-alert-grouping",
    "https://support.pagerduty.com/main/docs/content-based-alert-grouping",
    "https://support.pagerduty.com/main/docs/unified-alert-grouping",
    "https://support.pagerduty.com/main/docs/global-alert-grouping",
    "https://support.pagerduty.com/main/docs/time-based-alert-grouping",
    "https://support.pagerduty.com/main/docs/auto-pause-incident-notifications",
    "https://support.pagerduty.com/main/docs/event-orchestration",
    "https://support.pagerduty.com/main/docs/event-orchestration-cache-variables",
    "https://support.pagerduty.com/main/docs/past-incidents",
    "https://support.pagerduty.com/main/docs/related-incidents",
    "https://support.pagerduty.com/main/docs/outlier-incident",
    "https://support.pagerduty.com/main/docs/probable-origin",
    "https://support.pagerduty.com/main/docs/recent-changes",
    "https://support.pagerduty.com/main/docs/event-orchestration-examples",
    "https://support.pagerduty.com/main/docs/operations-console",
    "https://support.pagerduty.com/main/docs/legacy-event-intelligence",
    "https://support.pagerduty.com/main/docs/rulesets",
    "https://support.pagerduty.com/main/docs/migrate-to-event-orchestration",
    "https://support.pagerduty.com/main/docs/analytics-dashboard",
    "https://support.pagerduty.com/main/docs/insights",
    "https://support.pagerduty.com/main/docs/operational-reviews",
    "https://support.pagerduty.com/main/docs/on-call-readiness-reports",
    "https://support.pagerduty.com/main/docs/event-analytics",
    "https://support.pagerduty.com/main/docs/pagerduty-advance-analytics",
    "https://support.pagerduty.com/main/docs/user-onboarding-report",
    "https://support.pagerduty.com/main/docs/recommendations",
    "https://support.pagerduty.com/main/docs/audit-trail-reporting",
    "https://support.pagerduty.com/main/docs/pagerduty-analytics-slack-integration",
    "https://support.pagerduty.com/main/docs/operational-maturity",
    "https://developer.pagerduty.com/docs/introduction",
    "https://support.pagerduty.com/main/docs/api-access-keys",
    "https://support.pagerduty.com/main/docs/rest-api-rate-limits",
    "https://developer.pagerduty.com/docs/api-client-libraries",
    "https://support.pagerduty.com/main/docs/safelist-ips",
    "https://support.pagerduty.com/main/docs/third-party-tools",
    "https://developer.pagerduty.com/docs/api-tools-and-code-samples",
    "https://support.pagerduty.com/main/docs/status-pages-overview",
    "https://support.pagerduty.com/main/docs/internal-status-page",
    "https://support.pagerduty.com/main/docs/external-status-page",
    "https://support.pagerduty.com/main/docs/private-status-page",
    "https://support.pagerduty.com/main/docs/billing-invoices-payments",
    "https://support.pagerduty.com/main/docs/w-9",
    "https://support.pagerduty.com/main/docs/vendor-form",
    "https://support.pagerduty.com/main/docs/cancel-your-account",
    "https://support.pagerduty.com/main/docs/account-settings",
    "https://support.pagerduty.com/main/docs/account-subdomains",
    "https://support.pagerduty.com/main/docs/time-zone-settings",
    "https://university.pagerduty.com/page/on-demand#new-to-pagerduty_getting-started",
    "https://support.pagerduty.com/main/docs/mobile-app",
    "https://support.pagerduty.com/main/docs/mobile-home-screen",
    "https://support.pagerduty.com/main/docs/mobile-widgets",
    "https://support.pagerduty.com/main/docs/mobile-status-dashboard",
    "https://support.pagerduty.com/main/docs/mobile-app-settings",
    "https://support.pagerduty.com/main/docs/use-mobile-schedules",
    "https://support.pagerduty.com/main/docs/home-screen-status-dashboard",
    "https://support.pagerduty.com/main/docs/mdm-setup-browsers",
    "https://support.pagerduty.com/main/docs/release-notes",
    "https://www.pagerduty.com/whats-new/",
    "https://support.pagerduty.com/main/docs/platform-release-notes",
    "https://support.pagerduty.com/main/docs/system-requirements",
    "https://support.pagerduty.com/main/docs/pd-cef",
    "https://support.pagerduty.com/main/docs/search",
    "https://support.pagerduty.com/main/docs/pagerduty-outage-notifications",
    "https://support.pagerduty.com/main/docs/service-regions",
    "https://support.pagerduty.com/main/docs/get-started-with-jeli",
    "https://support.pagerduty.com/main/docs/jeli-incidents",
    "https://support.pagerduty.com/main/docs/jeli-slackbot-commands",
    "https://support.pagerduty.com/main/docs/mitigate-an-incident",
    "https://support.pagerduty.com/main/docs/jeli-workflows",
    "https://support.pagerduty.com/main/docs/opportunities",
    "https://support.pagerduty.com/main/docs/basic-investigation-tutorial",
    "https://support.pagerduty.com/main/docs/opportunity-stages",
    "https://support.pagerduty.com/main/docs/opportunity-report",
    "https://support.pagerduty.com/main/docs/incident-review-templates",
    "https://support.pagerduty.com/main/docs/opportunity-tags",
    "https://support.pagerduty.com/main/docs/related-opportunities",
    "https://support.pagerduty.com/main/docs/narrative-builder",
    "https://support.pagerduty.com/main/docs/narrative-builder-tutorial",
    "https://support.pagerduty.com/main/docs/see-participant-information",
    "https://support.pagerduty.com/main/docs/collect-action-items",
    "https://support.pagerduty.com/main/docs/opportunity-notes",
    "https://support.pagerduty.com/main/docs/opportunity-events",
    "https://support.pagerduty.com/main/docs/learning-center",
    "https://support.pagerduty.com/main/docs/view-people-in-jeli",
    "https://support.pagerduty.com/main/docs/jeli-settings-and-integrations",
    "https://support.pagerduty.com/main/docs/entra-id-integration-jeli",
    "https://support.pagerduty.com/main/docs/google-meet-integration-jeli",
    "https://support.pagerduty.com/main/docs/jira-integration-jeli",
    "https://support.pagerduty.com/main/docs/nobl9-integration-jeli",
    "https://support.pagerduty.com/main/docs/okta-integration-jeli",
    "https://support.pagerduty.com/main/docs/opsgenie-integration-jeli",
    "https://support.pagerduty.com/main/docs/pagerduty-integration-jeli",
    "https://support.pagerduty.com/main/docs/servicenow-integration-jeli",
    "https://support.pagerduty.com/main/docs/slack-integration-jeli",
    "https://support.pagerduty.com/main/docs/statuspage-integration-jeli",
    "https://support.pagerduty.com/main/docs/vanta-integration-jeli",
    "https://support.pagerduty.com/main/docs/zoom-integration-jeli",
    "https://support.pagerduty.com/main/docs/import-hr-data",
    "https://support.pagerduty.com/main/docs/jeli-api",
    "https://support.pagerduty.com/main/docs/pagerduty-and-cisa-0-day-vulnerability-remediation-timelines",
    "https://support.pagerduty.com/main/docs/pagerduty-log4j-zero-day-vulnerability",
    "https://support.pagerduty.com/main/docs/pagerduty-rundeck-automation-self-hosted-key-pair-misconfiguration",
    "https://support.pagerduty.com/main/docs/security-hygiene-for-the-current-cyber-threat-landscape",
    "https://support.pagerduty.com/main/docs/sisense-compromise",
    "https://support.pagerduty.com/main/docs/support-portal-faq",
    # Add more URLs as needed
]

# Local folder to store the docs
output_folder = "./pagerduty_docs"

def fetch_and_save(url):
    """Fetch content from a URL, convert it to Markdown, and save it locally."""
    try:
        response = requests.get(url, timeout=10)  # Add timeout to prevent long hangs
        response.raise_for_status()  # Raise HTTP errors (4xx, 5xx)

        soup = BeautifulSoup(response.text, "html.parser")
        content_div = soup.find("main") or soup.find("article") or soup.body

        if content_div:
            text_content = markdownify(str(content_div))
            filename = url.split("/")[-1] + ".md"
            filepath = os.path.join(output_folder, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text_content)

            print(f"✅ Saved: {filename}")
        else:
            print(f"⚠️ Could not extract content from {url}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch {url}: {e}")

# Fetch and save each URL with a delay
for url in pagerduty_urls:
    fetch_and_save(url)
    time.sleep(2)  # ✅ Add a 2-second delay between requests
