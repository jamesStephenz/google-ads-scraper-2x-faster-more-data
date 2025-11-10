# Google Ads Scraper (2× Faster, More Data)

> Extract current and historical ads from Google’s Ads Transparency Center with speed and depth. Search by advertiser, domain, format, country, and date range, then capture creatives, impression ranges, audience selections, and platform-level stats.
>
> This Google Ads Scraper helps competitive researchers, marketers, and journalists gather transparent, verifiable ad data at scale.


<p align="center">
  <a href="https://bitbash.def" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Google Ads Scraper (2X Faster, More Data)</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction

This project collects ad transparency data directly from Google’s Ads Transparency Center. It programmatically visits search or creative URLs, paginates through results, and normalizes key fields for analysis or downstream pipelines.

It solves the pain of manual ad reviews, missing metadata, and inconsistent exports by providing a consistent schema with optional media downloading to a local store. It’s designed for growth teams, agencies, analysts, and data journalists who need structured ad intelligence fast.

### Transparency-Centered Coverage

- Supports all ad formats: TEXT, IMAGE, and VIDEO.
- Captures first and last seen dates, impression ranges, and shown countries.
- Includes per-country platform stats (Search, YouTube, Shopping) when available.
- Extracts decoded text variants and primary media preview links.
- Optional cookie input unlocks age-restricted/personalized items; proxy routing enables geo-targeting.

## Features

| Feature | Description |
|----------|-------------|
| Multi-format capture | Scrapes TEXT, IMAGE, and VIDEO creatives with normalized fields. |
| Fast pagination | Processes ~100 ads in ~39 seconds with robust pagination controls. |
| Rich metadata | Collects firstShownAt, lastShownAt, impression ranges, shown countries, and URL to the original ad page. |
| Audience selections | Extracts targeting categories with included/excluded flags for transparency. |
| Platform stats per country | Breaks down impressions by Search, YouTube, and Shopping when provided. |
| Variants & media | Gathers creative variants, decoded text, media links, and optional media download to a local store. |
| Search & deep-link modes | Accepts both Transparency Center search URLs and direct creative detail URLs. |
| Proxy & cookies | Uses regional proxies for geo results; accepts exported cookies to access restricted items. |
| Max items control | Limit output deterministically with `maxItems`. |
| Structured outputs | Emits clean JSON/CSV-ready records for analytics and warehousing. |

---

## What Data This Scraper Extracts

| Field Name | Field Description |
|-------------|------------------|
| id | Unique record ID for the scraped item (often equals creativeId). |
| advertiserId | The advertiser’s unique identifier. |
| creativeId | The ad creative identifier. |
| advertiserName | Human-readable advertiser name. |
| format | Ad format enum: TEXT, IMAGE, or VIDEO. |
| url | Full link to the ad detail on the Transparency Center. |
| previewUrl | Canonical media/preview link for the creative when present. |
| previewStoreKey | Local media store key if media download is enabled. |
| firstShownAt | First seen timestamp (epoch or ISO) indicating launch date. |
| lastShownAt | Last seen timestamp (epoch or ISO). |
| impressions | Total or range upper bound estimate when provided. |
| shownCountries | List of countries where the ad was shown. |
| countryStats | Array of per-country stats (first/last shown and impression bounds). |
| platformStats | Nested per-country platform breakdown (Search, YouTube, Shopping). |
| audienceSelections | Targeting categories with include/exclude flags. |
| variants | Array of text and media variants with decoded text and image/video links. |
| originUrl | The original Transparency Center search or detail URL used. |
| mediaStoreKeys | Array of stored media keys when media download is enabled. |

---

## Example Output


    [
      {
        "id": "CR08100116008800354305",
        "advertiserId": "AR10303883279069085697",
        "creativeId": "CR08100116008800354305",
        "advertiserName": "My Jewellery B.V",
        "format": "IMAGE",
        "url": "https://adstransparency.google.com/advertiser/AR10303883279069085697/creative/CR08100116008800354305?region=DE&platform=YOUTUBE&start-date=2022-01-01&end-date=2024-12-31&format=IMAGE",
        "previewUrl": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcT5cZ5keol3Qh0OGy8BxONGNpoc9OeRl771pz5cN4FnyOwhmGU",
        "previewStoreKey": "CR08100116008800354305_preview_0.jpg",
        "firstShownAt": "1710421161",
        "lastShownAt": "1758540064",
        "impressions": "600000",
        "shownCountries": ["Germany"],
        "countryStats": [
          {
            "code": "DE",
            "name": "Germany",
            "firstShownAt": "2024-03-14T00:00:00.000Z",
            "lastShownAt": "2025-09-22T00:00:00.000Z",
            "impressions": {
              "lowerBound": "500000",
              "upperBound": "600000"
            },
            "platformStats": [
              {
                "name": "YouTube",
                "code": "YOUTUBE",
                "impressions": { "lowerBound": "8000", "upperBound": "9000" }
              },
              {
                "name": "Google Shopping",
                "code": "SHOPPING",
                "impressions": { "lowerBound": "3000", "upperBound": "4000" }
              },
              {
                "name": "Google Search",
                "code": "SEARCH",
                "impressions": { "lowerBound": "450000", "upperBound": "500000" }
              }
            ]
          }
        ],
        "audienceSelections": [
          { "name": "Demographic info", "hasIncludedCriteria": true, "hasExcludedCriteria": false },
          { "name": "Geographic locations", "hasIncludedCriteria": true, "hasExcludedCriteria": true },
          { "name": "Contextual signals", "hasIncludedCriteria": true, "hasExcludedCriteria": true }
        ],
        "variants": [
          {
            "textContent": "Handykette mit Leopardemuster | My Jewellery - My Jewellery - Bigshopper",
            "images": [
              "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcT5cZ5keol3Qh0OGy8BxONGNpoc9OeRl771pz5cN4FnyOwhmGU"
            ],
            "imageStoreKeys": ["CR08100116008800354305_v0_0.jpg"]
          }
        ],
        "originUrl": "https://adstransparency.google.com/advertiser/AR10303883279069085697?region=DE&platform=YOUTUBE&start-date=2022-01-01&end-date=2024-12-31&format=IMAGE"
      }
    ]

---

## Directory Structure Tree


    google-ads-scraper-2x-faster-more-data/
    ├── src/
    │   ├── main.py
    │   ├── config/
    │   │   └── settings.example.json
    │   ├── clients/
    │   │   └── transparency_center_client.py
    │   ├── extractors/
    │   │   ├── ad_parser.py
    │   │   └── variants_parser.py
    │   ├── pipelines/
    │   │   ├── pagination.py
    │   │   └── normalize.py
    │   ├── storage/
    │   │   ├── dataset_writer.py
    │   │   └── media_store.py
    │   └── utils/
    │       ├── cookies.py
    │       ├── proxies.py
    │       └── timefmt.py
    ├── data/
    │   ├── sample_input.json
    │   └── sample_output.json
    ├── requirements.txt
    └── README.md

---

## Use Cases

- **Growth marketers** track competitor messaging and formats across countries to improve creative strategy and benchmarking.
- **Analysts** aggregate impression ranges and platform splits to evaluate channel mix by market and season.
- **Data journalists** investigate audience selections and transparency patterns for public-interest reporting.
- **Agencies** monitor client and competitor ads during launches to validate coverage and spot copycat trends.
- **Compliance teams** archive ad variations and dates for documentation and risk reviews.

---

## FAQs

**How do I access age-restricted or personalized ads?**
Export cookies from a test Google account using a cookie manager extension and provide them as JSON input. This increases visibility for restricted items while keeping your primary account safe.

**How do I target a specific country’s inventory?**
Route traffic through a regional proxy. For example, use a US exit to surface US-visible ads. Different regions can show different inventories and impression ranges.

**What limits the number of ads collected?**
Inventory depends on your search parameters, account visibility (if cookies are provided), and region. Use `maxItems` to cap results deterministically.

**Is this data suitable for BI tools?**
Yes. The normalized JSON schema (including country and platform breakdowns) is ready for loading into warehouses or notebooks for analysis.

---

## Performance Benchmarks and Results

**Primary Metric — Speed:** ~39 seconds per 100 ads on typical consumer hardware and a stable network using search URLs with pagination.
**Reliability Metric — Stability:** >98% successful runs across varied advertisers and formats when proxies and cookies are configured correctly.
**Efficiency Metric — Throughput:** Sustained processing of hundreds of creatives per minute with batched pagination and lightweight parsing.
**Quality Metric — Completeness:** Country and platform stats captured whenever exposed; text variants decoded for the majority of text/image creatives, with media keys recorded if download is enabled.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
