document.addEventListener('DOMContentLoaded', function() {
  // Получение элементов формы и списка марок
  var markSelect = document.getElementById('markSelect');
  var modelList = document.getElementById('modelList');
  var submitBtn = document.getElementById('submitBtn');

  // Обработчик события нажатия на кнопку
  submitBtn.addEventListener('click', function() {
    var selectedMarkId = markSelect.value;

    // Загрузка списка моделей для выбранной марки
    fetch(`/models/?mark_id=${selectedMarkId}`, {
      headers: {
        'Accept': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => {
        // Очистка списка моделей перед обновлением
        modelList.innerHTML = '';

        // Заполнение списка моделей
        data.forEach(model => {
          var modelItem = document.createElement('p');
          modelItem.textContent = model.name;
          modelList.appendChild(modelItem);
        });
      })
      .catch(error => console.error('Error loading models:', error));
  });
});