"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const client_1 = require("@prisma/client");
const prisma = new client_1.PrismaClient({
    log: ['info'],
});
async function main() {
    console.log('Seeding database...');
    const categories = [
        {
            name: 'Rings',
            slug: 'rings',
            description: 'Elegant rings for every occasion.',
        },
        {
            name: 'Necklaces',
            slug: 'necklaces',
            description: 'Timeless necklaces to adorn your neck.',
        },
        {
            name: 'Earrings',
            slug: 'earrings',
            description: 'Stunning earrings that catch the light.',
        },
        {
            name: 'Bracelets',
            slug: 'bracelets',
            description: 'Sophisticated bracelets for a delicate touch.',
        },
    ];
    for (const cat of categories) {
        await prisma.category.upsert({
            where: { slug: cat.slug },
            update: {},
            create: cat,
        });
    }
    const ringsCategory = await prisma.category.findUnique({ where: { slug: 'rings' } });
    const necklacesCategory = await prisma.category.findUnique({ where: { slug: 'necklaces' } });
    const earringsCategory = await prisma.category.findUnique({ where: { slug: 'earrings' } });
    const products = [
        {
            name: 'Eternity Diamond Ring',
            slug: 'eternity-diamond-ring',
            description: 'A stunning band of continuous diamonds symbolizing eternal love. Crafted in 18k White Gold.',
            price: 1299.00,
            stock: 10,
            images: ['https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=800&q=80'],
            status: client_1.ProductStatus.PUBLISHED,
            categoryId: ringsCategory?.id,
        },
        {
            name: 'Gold Signet Ring',
            slug: 'gold-signet-ring',
            description: 'A classic signet ring with a modern twist. 18k Yellow Gold.',
            price: 550.00,
            stock: 15,
            images: ['https://images.unsplash.com/photo-1622398925373-3f91b1e275f5?auto=format&fit=crop&w=800&q=80'],
            status: client_1.ProductStatus.PUBLISHED,
            categoryId: ringsCategory?.id,
        },
        {
            name: 'Sapphire Pendant Necklace',
            slug: 'sapphire-pendant-necklace',
            description: 'A deep blue sapphire surrounded by a halo of diamonds. 18k White Gold chain.',
            price: 899.00,
            stock: 8,
            images: ['https://images.unsplash.com/photo-1599643478518-17488fbbcd75?auto=format&fit=crop&w=800&q=80'],
            status: client_1.ProductStatus.PUBLISHED,
            categoryId: necklacesCategory?.id,
        },
        {
            name: 'Pearl Drop Earrings',
            slug: 'pearl-drop-earrings',
            description: 'Elegant freshwater pearls suspended from a gold hook. Timeless beauty.',
            price: 250.00,
            stock: 20,
            images: ['https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=800&q=80'],
            status: client_1.ProductStatus.PUBLISHED,
            categoryId: earringsCategory?.id,
        },
        {
            name: 'Vintage Solitaire Ring',
            slug: 'vintage-solitaire-ring',
            description: 'A vintage-inspired solitaire ring featuring a round brilliant cut diamond.',
            price: 2100.00,
            stock: 5,
            images: ['https://images.unsplash.com/photo-1589674781759-c21c37956a44?auto=format&fit=crop&w=800&q=80'],
            status: client_1.ProductStatus.PUBLISHED,
            categoryId: ringsCategory?.id,
        },
        {
            name: 'Rose Gold Choker',
            slug: 'rose-gold-choker',
            description: 'A minimalist choker crafted in 14k Rose Gold. Perfect for layering.',
            price: 450.00,
            stock: 12,
            images: ['https://images.unsplash.com/photo-1602173574767-37ac01994b2a?auto=format&fit=crop&w=800&q=80'],
            status: client_1.ProductStatus.PUBLISHED,
            categoryId: necklacesCategory?.id,
        },
        {
            name: 'Emerald Studs',
            slug: 'emerald-studs',
            description: 'Vibrant emeralds set in a simple 4-prong gold setting.',
            price: 320.00,
            stock: 18,
            images: ['https://images.unsplash.com/photo-1589674781759-c21c37956a44?auto=format&fit=crop&w=800&q=80'],
            status: client_1.ProductStatus.PUBLISHED,
            categoryId: earringsCategory?.id,
        }
    ];
    for (const product of products) {
        await prisma.product.upsert({
            where: { slug: product.slug },
            update: {},
            create: product,
        });
    }
    console.log('Seeding finished.');
}
main()
    .catch((e) => {
    console.error(e);
    process.exit(1);
})
    .finally(async () => {
    await prisma.$disconnect();
});
//# sourceMappingURL=seed.js.map