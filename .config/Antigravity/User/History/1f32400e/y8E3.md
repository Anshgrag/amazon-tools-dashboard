# Jewellery Platform Upgrade Plan

## Goal Description
Transform the current basic prototype into a premium, production-ready jewellery e-commerce platform. This involves a complete UI/UX overhaul to match luxury design standards (minimalist, elegant, smooth animations), populating the database with realistic sample products, and ensuring all core e-commerce flows (browse, view, cart, checkout simulation) are polished and functional.

## User Review Required
> [!IMPORTANT]
> **Design Assets**: I will use placeholder images from Unsplash via a seeding script. If you have specific product photography, you will need to replace the URLs in the database later.

> [!NOTE]
> **Authentication**: I will implement a basic JWT auth flow. For "Ready to Deploy" status, ensure you update the `.env` file with your actual secret keys and database credentials in production.

## Proposed Changes

### Backend (`server`)

#### [NEW] `prisma/seed.ts`
- Create a seeding script to populate:
    - **Categories**: Rings, Necklaces, Earrings, Bracelets.
    - **Products**: ~10-20 high-quality sample items with descriptions, prices, and Unsplash image URLs.
- Update `package.json` to include a `seed` script.

#### [MODIFY] `src/app.module.ts`
- Ensure `ServeStaticModule` is configured (if serving client build) or ensure CORS is set up for separate client/server deployment.

### Frontend (`client`)

#### [MODIFY] `src/app/globals.css`
- Import premium fonts (e.g., *Playfair Display*, *Lato*).
- Define CSS variables for luxury color palette (Gold, Charcoal, Cream).
- specific utility classes for typography and spacing.

#### [MODIFY] `src/components/Navbar.tsx`
- Implement transparent-to-solid transition on scroll.
- Improve typography and spacing.
- Add Cart icon with badge (connected to Zustand store).

#### [MODIFY] `src/app/page.tsx` (Homepage)
- **Hero Section**: Full-height, distinct "CTA", background image/video.
- **Featured Section**: Carousel of top products.
- **Category Grid**: Visual grid of categories.

#### [NEW] `src/components/ProductCard.tsx`
- Minimalist card with hover effect (secondary image reveal).
- "Quick Add" button.

#### [MODIFY] `src/app/products/page.tsx`
- Implement Grid/List view.
- Add Sidebar for Filters (Price, Category).

#### [MODIFY] `src/app/products/[slug]/page.tsx`
- Product Image Gallery (Thumbnails + Main image).
- Description, Specifications (Material, Weight).
- Related Products section.

#### [NEW] `src/store/cartStore.ts`
- Zustand store for managing cart state (persist to local storage).

#### [NEW] `src/components/CartDrawer.tsx`
- Slide-out cart for quick review.

## Verification Plan

### Automated Tests
- Run `npm run build` in both `client` and `server` to ensure no build errors.
- Run `npm run lint` to check for code quality issues.
- Run `npx prisma db seed` to verify data population works without errors.

### Manual Verification
1.  **Homepage**: Verify hero loads, nav works, layout is responsive.
2.  **Browsing**: Go to `/products`, filter by category, check loading states.
3.  **Product Detail**: Click a product, verify images load, info is correct, "Add to Cart" updates the cart count.
4.  **Cart**: Open cart drawer, verify total calculation, remove item.
5.  **Responsiveness**: Check on mobile view (chrome dev tools) for broken layouts.
