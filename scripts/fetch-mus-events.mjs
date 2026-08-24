#!/usr/bin/env node
/**
 * Eventfrog Public API → data/mus_export.json
 *
 * Gleiches Coucou-Record-Layout wie in prototype-hvw-website
 * (cronjobs/eventfrog_to_mus.py), nur OrgID 5116588 (Museum Schaffen).
 *
 *   EVENTFROG_API_KEY=<key> node scripts/fetch-mus-events.mjs
 */

import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const API_BASE = "https://api.eventfrog.net";
const ORG_IDS = ["5116588"];
const OUTPUT_PATH = fileURLToPath(new URL("../data/mus_export.json", import.meta.url));

const RUBRIC_TO_COUCOU = [
  ["konzert", 69],
  ["party", 70],
  ["film", 11],
  ["literatur", 14],
  ["theater", 71],
  ["tanz", 72],
  ["ausstellung", 13],
  ["vernissage", 217],
  ["kinder", 213],
  ["führung", 280],
  ["fuehrung", 280],
  ["vortrag", 281],
];
const DEFAULT_CATEGORY = 15;

const apiKey = (process.env.EVENTFROG_API_KEY || "").trim();
if (!apiKey) {
  console.error(
    "Error: EVENTFROG_API_KEY is not set.\n" +
      "GitHub Actions Secret EVENTFROG_API_KEY (Eventfrog Public API key) hinterlegen."
  );
  process.exit(1);
}

async function fetchJson(path, params) {
  const url = new URL(path, API_BASE);
  for (const [key, value] of Object.entries(params)) {
    if (Array.isArray(value)) value.forEach((v) => url.searchParams.append(key, v));
    else if (value != null) url.searchParams.set(key, value);
  }
  const res = await fetch(url, { headers: { Authorization: `Bearer ${apiKey}` } });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`Eventfrog API ${res.status} ${res.statusText} for ${url}\n${body}`);
  }
  return res.json();
}

function pickLang(field) {
  if (!field) return "";
  if (typeof field === "string") return field;
  return field.de || field.de_CH || field.en || field.fr || Object.values(field).find(Boolean) || "";
}

function stripHtml(html) {
  if (!html) return "";
  return html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
}

function parseIso(iso) {
  if (!iso) return null;
  const d = new Date(iso);
  return Number.isNaN(d.getTime()) ? null : d;
}

function dateStr(iso) {
  const d = parseIso(iso);
  if (!d) {
    const s = String(iso || "");
    if (s.length >= 10 && s[4] === "-" && s[7] === "-") {
      return `${s.slice(0, 4)}/${s.slice(5, 7)}/${s.slice(8, 10)}`;
    }
    return "";
  }
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}/${m}/${day}`;
}

function timeStr(iso) {
  const d = parseIso(iso);
  if (!d) return "";
  return `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
}

function pickImage(event) {
  const candidates = [
    event.emblemToShow?.url,
    event.image?.url,
    event.imageUrl,
    event.flyerUrl,
    typeof event.image === "string" ? event.image : "",
    Array.isArray(event.images) ? event.images[0]?.url || event.images[0] : "",
  ];
  for (const value of candidates) {
    if (typeof value === "string" && /^https?:\/\//.test(value)) return value.split("?")[0];
  }
  return "";
}

async function fetchOgImage(eventUrl) {
  if (!eventUrl || !/^https?:\/\//.test(eventUrl)) return "";
  try {
    const res = await fetch(eventUrl, {
      headers: { Accept: "text/html", "User-Agent": "MuS-Website-events/1.0" },
      redirect: "follow",
    });
    if (!res.ok) return "";
    const html = await res.text();
    const match =
      html.match(/property=["']og:image["']\s+content=["']([^"']+)/i) ||
      html.match(/content=["']([^"']+)["']\s+property=["']og:image["']/i);
    const image = match?.[1]?.trim() || "";
    return /^https?:\/\//.test(image) ? image.split("?")[0] : "";
  } catch {
    return "";
  }
}

function mapCategory(rubric, rubricsById) {
  const title = pickLang(rubricsById[rubric]?.title).toLowerCase();
  for (const [keyword, id] of RUBRIC_TO_COUCOU) {
    if (title.includes(keyword)) return id;
  }
  return DEFAULT_CATEGORY;
}

async function main() {
  const today = new Date().toISOString().slice(0, 10);
  const events = [];
  let page = 1;
  while (true) {
    const data = await fetchJson("/public/v1/events", {
      orgId: ORG_IDS,
      perPage: 100,
      page,
      country: "CH",
      from: today,
    });
    const batch = data.events || [];
    events.push(...batch);
    if (!batch.length || events.length >= (data.totalNumberOfResources || batch.length)) break;
    page += 1;
  }

  events.sort((a, b) => String(a.begin || "").localeCompare(String(b.begin || "")));

  const locationIds = [...new Set(events.flatMap((e) => e.locationIds || []))];
  let locationsById = {};
  if (locationIds.length) {
    const { locations = [] } = await fetchJson("/public/v1/locations", { id: locationIds });
    locationsById = Object.fromEntries(locations.map((loc) => [loc.id, loc]));
  }

  let rubricsById = {};
  try {
    const { rubrics = [] } = await fetchJson("/public/v1/rubrics", {});
    rubricsById = Object.fromEntries(rubrics.map((r) => [r.id, r]));
  } catch {
    /* optional */
  }

  const result = [];
  for (const event of events) {
    const location = locationsById[event.locationIds?.[0]];
    const descriptionHtml = pickLang(event.descriptionAsHTML);
    const descriptionLong = stripHtml(descriptionHtml);
    const shortDescription = pickLang(event.shortDescription);
    let image = pickImage(event);
    if (!image && event.url) image = await fetchOgImage(event.url);

    const date = dateStr(event.begin);
    const dateEnd = dateStr(event.end);
    const record = {
      reference: String(event.id ?? ""),
      title: pickLang(event.title),
      description: shortDescription || descriptionLong,
      url: event.url,
      date,
      time_start: timeStr(event.begin),
      time_end: timeStr(event.end),
      category: mapCategory(event.rubricId, rubricsById),
    };
    if (image) record.image = image;
    if (event.lowestTicketPrice) record.fee = event.lowestTicketPrice;
    if (event.presaleLink) record.presale = event.presaleLink;
    if (descriptionLong) record.description_long = descriptionLong;
    if (descriptionHtml) record.description_html = descriptionHtml;
    if (dateEnd && dateEnd !== date) record.date_end = dateEnd;
    if (location) {
      record.location_name = pickLang(location.title);
      if (location.addressLine) record.location_street = location.addressLine;
      if (location.zip) record.location_zip = location.zip;
      if (location.city) record.location_city = location.city;
      if (location.websiteUrl) record.location_website = location.websiteUrl;
    }
    result.push(Object.fromEntries(Object.entries(record).filter(([, v]) => v !== "" && v != null)));
  }

  await writeFile(OUTPUT_PATH, `${JSON.stringify(result, null, 2)}\n`, "utf8");
  console.log(`Wrote ${result.length} Museum-Schaffen event(s) to ${OUTPUT_PATH}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
