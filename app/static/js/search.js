/* =====================================================
   Eagle Furniture Ngara
   Live AJAX Search
   Version 1.0
===================================================== */

document.addEventListener("DOMContentLoaded", () => {

    const searchInput = document.getElementById("live-search");
    const productGrid = document.getElementById("products-grid");
    const productCount = document.getElementById("product-count");
    const emptyProducts = document.getElementById("empty-products");

    if (!searchInput || !productGrid) return;

    async function searchProducts() {

        const query = searchInput.value.trim();

        try {

            const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);

            const products = await response.json();

            renderProducts(products);

        } catch (error) {

            console.error("Search Error:", error);

        }

    }

    function renderProducts(products) {

        productGrid.innerHTML = "";

        productCount.textContent = products.length;

        if (products.length === 0) {

            productGrid.style.display = "none";
            emptyProducts.style.display = "block";

            return;

        }

        productGrid.style.display = "grid";
        emptyProducts.style.display = "none";

        products.forEach(product => {

            const card = `

                <div class="product-card">

                    <div class="product-image">

                        <a href="/product/${product.id}">

                            <img
                                src="/static/${product.image}"
                                alt="${product.name}"
                            >

                        </a>

                        ${product.featured
                            ? `<span class="product-badge">Featured</span>`
                            : ""
                        }

                    </div>

                    <div class="product-content">

                        <span class="product-category">

                            ${product.category}

                        </span>

                        <h3>

                            <a href="/product/${product.id}">

                                ${product.name}

                            </a>

                        </h3>

                        <div class="product-price">

                            KSh ${Number(product.price).toLocaleString()}

                        </div>

                        <div class="product-actions">

                            <a
                                href="/product/${product.id}"
                                class="btn btn-outline"
                            >
                                View Details
                            </a>

                            <button
                                class="btn btn-primary add-cart"
                                data-id="${product.id}"
                            >
                                Add to Cart
                            </button>

                        </div>

                    </div>

                </div>

            `;

            productGrid.insertAdjacentHTML("beforeend", card);

        });

    }

    let timer;

    searchInput.addEventListener("keyup", () => {

        clearTimeout(timer);

        timer = setTimeout(searchProducts, 300);

    });

});