Source: https://laravel.com/cloud/docs/compliance.md

# Compliance & Security

Learn about Laravel Cloud security practices, compliance controls, and protections for production apps.

Security and compliance are critical for your business, and we take both seriously. This page describes Laravel Cloud's current compliance status and the security measures that protect your applications.

## Current compliance status

### SOC 2 Type 2

System and Organization Control 2 Type 2 (SOC 2) is a compliance framework developed by the American Institute of Certified Public Accountants (AICPA) that focuses on how an organization's services remain secure and protect customer data. The framework has 5 Trust Services Categories (TSCs). Each category contains criteria to evaluate the controls and service commitments of an organization.

Laravel Cloud has achieved SOC 2 Type 2 attestation for Security, Confidentiality, and Availability.

More information is available at [trust.laravel.com](https://trust.laravel.com/?product=cloud).

### HIPAA

The Health Insurance Portability and Accountability Act (HIPAA) sets national standards for protecting sensitive patient health information in the United States.

Laravel Cloud supports HIPAA compliance for customers on our Enterprise and Private Cloud plans. That support includes a signed Business Associate Agreement (BAA) and the administrative, physical, and technical safeguards required to protect Protected Health Information (PHI).

> [!NOTE]
>
> If your application handles PHI, contact our team at [cloud@laravel.com](mailto:cloud@laravel.com) to request a BAA before deploying to Laravel Cloud.

More information is available at [trust.laravel.com](https://trust.laravel.com/?product=cloud).

### ISO 27001

Laravel Cloud has achieved ISO 27001 certification. This internationally recognized standard for information security management systems helps protect your data and ensure the confidentiality, integrity, and availability of our platform.

## What this means for you

These standards shape how we handle your data and run the platform:

* We protect your data from unauthorized access, use, disclosure, disruption, modification, or destruction.
* For OWASP Top 10 coverage, Cloudflare's [OWASP Core Ruleset](https://developers.cloudflare.com/waf/managed-rules/reference/owasp-core-ruleset/) protects every domain served through Laravel Cloud's edge network, including default domains and custom domains proxied through Cloudflare. The ruleset filters common injection, authentication, and data exposure attacks before they reach your application.
* We keep the platform running continuously and work to minimize downtime.
* We keep your data private and prevent unauthorized access.
* We follow industry best practices and regulatory requirements.

## Stay updated

We update this page as our compliance status changes, so check back for the latest information. If you have questions about our compliance status, contact our support team at [cloud@laravel.com](mailto:cloud@laravel.com).

Thank you for trusting Laravel Cloud with your applications.
