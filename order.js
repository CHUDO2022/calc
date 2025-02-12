document.addEventListener('DOMContentLoaded', () => { 
    const urlParams = new URLSearchParams(window.location.search);
    const productData = JSON.parse(urlParams.get('product_data'));

    if (!productData) {
        alert("Нет данных о продукте в URL");
        return;
    }

    const telegramUser = JSON.parse(localStorage.getItem('telegramUser'));

    if (!telegramUser) {
        alert("Данные пользователя не найдены.");
        return;
    }

    // Отображение изображений товара
    const imageSlider = document.getElementById('image-slider');
    const imageDots = document.getElementById('image-dots');
    const images = productData.images || [];
    let currentImageIndex = 0;

    function updateImageSlider() {
        if (images.length > 0) {
            imageSlider.innerHTML = `<img src="${images[currentImageIndex]}" class="slider-img">`;
            updateImageDots();
        } else {
            imageSlider.innerHTML = `<p>Изображения отсутствуют</p>`;
        }
    }

    function updateImageDots() {
        imageDots.innerHTML = '';
        images.forEach((_, index) => {
            const dot = document.createElement('span');
            dot.classList.add('dot');
            if (index === currentImageIndex) {
                dot.classList.add('active');
            }
            dot.addEventListener('click', () => {
                currentImageIndex = index;
                updateImageSlider();
            });
            imageDots.appendChild(dot);
        });
    }

    imageSlider.addEventListener('click', (event) => {
        if (event.clientX < window.innerWidth / 2) {
            currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
        } else {
            currentImageIndex = (currentImageIndex + 1) % images.length;
        }
        updateImageSlider();
    });

    // Добавление свайпа для смартфонов
    let touchStartX = 0;
    let touchEndX = 0;

    imageSlider.addEventListener('touchstart', (event) => {
        touchStartX = event.changedTouches[0].screenX;
    });

    imageSlider.addEventListener('touchend', (event) => {
        touchEndX = event.changedTouches[0].screenX;
        handleSwipe();
    });

    function handleSwipe() {
        if (touchEndX < touchStartX) {
            currentImageIndex = (currentImageIndex + 1) % images.length;
        }
        if (touchEndX > touchStartX) {
            currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
        }
        updateImageSlider();
    }

    updateImageSlider();

    // Отображение отзывов
    const reviewsSlider = document.getElementById('reviews-slider');
    const reviewDots = document.getElementById('review-dots');
    const reviews = productData.reviews || [];
    let currentReviewIndex = 0;

    function updateReviewsSlider() {
        if (reviews.length > 0) {
            reviewsSlider.innerHTML = `<img src="${reviews[currentReviewIndex]}" class="slider-img">`;
            updateReviewDots();
        } else {
            reviewsSlider.innerHTML = `<p>Отзывы отсутствуют</p>`;
        }
    }

    function updateReviewDots() {
        reviewDots.innerHTML = '';
        reviews.forEach((_, index) => {
            const dot = document.createElement('span');
            dot.classList.add('dot');
            if (index === currentReviewIndex) {
                dot.classList.add('active');
            }
            dot.addEventListener('click', () => {
                currentReviewIndex = index;
                updateReviewsSlider();
            });
            reviewDots.appendChild(dot);
        });
    }

    reviewsSlider.addEventListener('click', (event) => {
        if (event.clientX < window.innerWidth / 2) {
            currentReviewIndex = (currentReviewIndex - 1 + reviews.length) % reviews.length;
        } else {
            currentReviewIndex = (currentReviewIndex + 1) % reviews.length;
        }
        updateReviewsSlider();
    });

    updateReviewsSlider();

    // Обновление информации о продукте
    document.getElementById('product-name').textContent = productData.name;
    document.getElementById('product-price').textContent = `${productData.price} ₽`;
    if (productData.old_price) {
        document.getElementById('product-old-price').textContent = `Старая цена: ${productData.old_price} ₽`;
    }
    document.getElementById('stock-status').textContent = productData.in_stock === 'Да' ? 'В наличии' : 'Нет в наличии';
    document.getElementById('product-description').textContent = productData.description;

    // Обработка кнопки "Перейти к оплате"
    const payButton = document.getElementById('pay-button');
    const modal = document.getElementById("modal");

    payButton.addEventListener('click', () => {
        if (productData.in_stock !== 'Да') {
            alert("Товар не в наличии");
            return; // Прерываем выполнение, если товар не в наличии
        }

        if (!modal) {
            alert("Модальное окно не найдено.");
            return;
        }
        modal.style.display = "block";
    });

    document.querySelector(".close").addEventListener('click', () => {
        modal.style.display = "none";
    });

    // Обработка отправки формы
    document.getElementById("user-form").addEventListener("submit", (event) => {
        event.preventDefault();

        const fullName = document.getElementById("full-name").value;
        const phoneNumber = document.getElementById("phone-number").value;
        const email = document.getElementById("email").value;

        const orderData = {
            product_id: productData.id,
            user_data: {
                user_id: telegramUser.id,
                full_name: fullName,
                phone_number: phoneNumber,
                email: email,
                username: telegramUser.username
            }
        };

        fetch('https://gadgetmark.ru/validate-order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(orderData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                modal.style.display = "none";
                window.location.href = "https://t.me/QSale_iphone_bot";
                console.log("Сверните окно");

                
            } else {
                alert(`Ошибка при отправке заказа: ${data.message}`);
            }
        })
        .catch(error => {
            alert("Произошла ошибка при отправке заказа.");
            console.error('Error:', error);
        });
    });
});
