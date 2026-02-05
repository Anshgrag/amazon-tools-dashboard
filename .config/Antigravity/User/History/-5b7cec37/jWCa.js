const { Client } = require('pg');
const fs = require('fs');
const path = require('path');

// Simple dotenv parser
function loadEnv() {
    try {
        const envPath = path.resolve(__dirname, '../.env');
        const envFile = fs.readFileSync(envPath, 'utf8');
        envFile.split('\n').forEach(line => {
            const parts = line.split('=');
            if (parts.length >= 2 && !line.startsWith('#')) {
                const key = parts[0].trim();
                const value = parts.slice(1).join('=').trim().replace(/^"|"$/g, '');
                process.env[key] = value;
            }
        });
    } catch (e) {
        console.log('No .env file found or error reading it');
    }
}

loadEnv();

const client = new Client({
    connectionString: process.env.DATABASE_URL,
});

async function main() {
    await client.connect();
    console.log('Connected to database via pg');

    // Categories
    const categories = [
        { name: 'Rings', slug: 'rings', description: 'Elegant rings.' },
        { name: 'Necklaces', slug: 'necklaces', description: 'Timeless necklaces.' },
        { name: 'Earrings', slug: 'earrings', description: 'Stunning earrings.' },
        { name: 'Bracelets', slug: 'bracelets', description: 'Sophisticated bracelets.' },
    ];

    for (const cat of categories) {
        const res = await client.query(
            `INSERT INTO "Category" (id, name, slug, description, "updatedAt") 
       VALUES (gen_random_uuid(), $1, $2, $3, NOW()) 
       ON CONFLICT (slug) DO UPDATE SET name = $1 RETURNING id`,
            [cat.name, cat.slug, cat.description]
        );
        cat.id = res.rows[0].id; // Store ID for products
    }

    // Products
    const products = [
        {
            name: 'Eternity Diamond Ring',
            slug: 'eternity-diamond-ring',
            description: 'A stunning band of continuous diamonds.',
            price: 1299.00,
            stock: 10,
            images: ['https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=800&q=80'],
            status: 'PUBLISHED',
            catSlug: 'rings'
        },
        {
            name: 'Sapphire Pendant',
            slug: 'sapphire-pendant',
            description: 'Deep blue sapphire with diamonds.',
            price: 899.00,
            stock: 8,
            images: ['https://images.unsplash.com/photo-1599643478518-17488fbbcd75?auto=format&fit=crop&w=800&q=80'],
            status: 'PUBLISHED',
            catSlug: 'necklaces'
        },
        {
            name: 'Gold Signet Ring',
            slug: 'gold-signet-ring',
            description: 'A classic signet ring.',
            price: 550.00,
            stock: 15,
            images: ['https://images.unsplash.com/photo-1622398925373-3f91b1e275f5?auto=format&fit=crop&w=800&q=80'],
            status: 'PUBLISHED',
            catSlug: 'rings'
        }
    ];

    for (const p of products) {
        const cat = categories.find(c => c.slug === p.catSlug);
        await client.query(
            `INSERT INTO "Product" (id, name, slug, description, price, stock, images, status, "categoryId", "updatedAt")
       VALUES (gen_random_uuid(), $1, $2, $3, $4, $5, $6, $7::"ProductStatus", $8, NOW())
       ON CONFLICT (slug) DO NOTHING`,
            [p.name, p.slug, p.description, p.price, p.stock, p.images, p.status, cat ? cat.id : null]
        );
    }

    console.log('Seeding complete');
    await client.end();
}

main().catch(e => {
    console.error(e);
    process.exit(1);
});
