# Project Specification: Commercial Cloud Deployment (Monetized)

## 1. Objective
Transform the **ChordDumper Music Theory Suite** into a commercial SaaS (Software as a Service) hosted on **Cloudflare Pages + Workers**, featuring usage-based throttling and newsletter/payment integration.

---

## 2. Commercial Tech Stack

### **Computing: Cloudflare Workers (TypeScript)**
- **Why TypeScript?** It is the "native" language of Cloudflare. It provides the best performance for handling thousands of users and has first-class support for **Stripe**, **KV Storage**, and **Rate Limiting**.
- **Logic Port:** The `engine.py` math will be ported to a `theory.ts` module.

### **Database & Throttling: Cloudflare KV (Key-Value)**
- **User State:** Store `{ "email": "status" }` (e.g., `free`, `pro`, `subscriber`).
- **Throttling:** Store a daily counter `{ "email:2024-04-14": 3 }`. If the counter > 5, the Worker returns an HTMX "Limit Reached" partial instead of a chord sheet.

### **Monetization Engine: Stripe + Newsletter Hooks**
- **Payments:** Use **Stripe Checkout** for subscriptions. Stripe sends a "Webhook" to your Worker when a payment succeeds to unlock "Pro" status.
- **Newsletter (Substack/Beehiiv):** Use a **Custom Webhook**. When a user confirms their subscription, your Worker adds their email to the "Allowed" list in KV.

---

## 3. The "Secure & Scale" Plan

### **Phase 1: The "Brain" Port (TypeScript)**
1.  Translate the `MOVABLE_VOICINGS` and `SCALES` dictionaries into a TypeScript `Constants.ts` file.
2.  Port the `detect_key_and_mood` and `get_nashville_number` logic to a clean, typed `TheoryEngine.ts`.

### **Phase 2: The Gatekeeper (Auth Worker)**
1.  **Login:** Use a **"Magic Link" (Email OTP)** system. No passwords. Cloudflare sends a code to their email; they enter it to get a 30-day session cookie.
2.  **Permission Check:** Every request to `/generate` first checks KV:
    - **If Subscriber:** Proceed.
    - **If Free User:** Increment daily counter. If > Limit, return "Please Subscribe" UI.
    - **If New:** Prompt to join newsletter.

### **Phase 3: Frontend (Cloudflare Pages)**
1.  Serve the `index.html` and Tailwind CSS as a static site via Cloudflare Pages.
2.  **HTMX Integration:** The frontend stays exactly as it is now, but instead of talking to a local Python server, it talks to your secure Cloudflare Worker at `/api/generate`.

---

## 4. Monetization Tiers (Example)

| Feature | Free Tier | Newsletter Subscriber | Pro Member ($5/mo) |
| :--- | :--- | :--- | :--- |
| **Generations** | 2 per day | 10 per day | Unlimited |
| **CAGED Shapes** | Basic | Full | Full + Advanced Jazz |
| **Practice Guide** | Preview Only | Full Printable | Full + Video Links |

---

## 5. Security & Rate Limiting
- **Cloudflare WAF:** Enable "Bot Fight Mode" to prevent scrapers from stealing your generated SVGs.
- **Zero Trust:** Use Cloudflare Access for **Admin Only** (you) to see the dashboard/analytics. Use the **Custom Auth Worker** for your customers.

---

## 6. Implementation Timeline
1.  **Week 1:** Port Python theory logic to TypeScript and test via CLI.
2.  **Week 2:** Build the KV-based throttling logic and the Magic Link login.
3.  **Week 3:** Connect Stripe/Newsletter webhooks and launch the Landing Page.
