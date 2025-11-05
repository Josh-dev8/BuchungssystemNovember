async function loadCategories() {
  const response = await fetch('/api/categories');
  if (!response.ok) {
    throw new Error('Kategorien konnten nicht geladen werden.');
  }
  return response.json();
}

async function loadTreatments(categoryId) {
  const response = await fetch(`/api/treatments/${categoryId}`);
  if (!response.ok) {
    throw new Error('Behandlungen konnten nicht geladen werden.');
  }
  return response.json();
}

function clearElement(element) {
  while (element.firstChild) {
    element.removeChild(element.firstChild);
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  const categorySelect = document.getElementById('categorySelect');
  const treatmentOptions = document.getElementById('treatmentOptions');
  const noOptionsHint = document.getElementById('noOptionsHint');

  try {
    const categories = await loadCategories();
    categories.forEach((category) => {
      const option = document.createElement('option');
      option.value = category.id;
      option.textContent = category.name;
      categorySelect.appendChild(option);
    });
  } catch (error) {
    noOptionsHint.textContent = error.message;
    noOptionsHint.classList.add('error');
    return;
  }

  categorySelect.addEventListener('change', async (event) => {
    const categoryId = event.target.value;
    clearElement(treatmentOptions);
    noOptionsHint.textContent = 'Lade Behandlungen…';
    noOptionsHint.classList.remove('error');
    noOptionsHint.classList.add('loading');

    try {
      const treatments = await loadTreatments(categoryId);
      clearElement(treatmentOptions);

      if (treatments.length === 0) {
        noOptionsHint.textContent = 'Für diese Kategorie sind aktuell keine Behandlungen hinterlegt.';
        noOptionsHint.classList.remove('loading');
        return;
      }

      treatments.forEach((treatment) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'option-button';
        button.textContent = `${treatment.name}`;
        button.addEventListener('click', () => {
          alert(`Sie haben "${treatment.name}" gewählt.`);
        });
        treatmentOptions.appendChild(button);
      });

      noOptionsHint.textContent = 'Bitte wählen Sie eine Behandlung aus.';
      noOptionsHint.classList.remove('loading');
    } catch (error) {
      clearElement(treatmentOptions);
      noOptionsHint.textContent = error.message;
      noOptionsHint.classList.add('error');
      noOptionsHint.classList.remove('loading');
    }
  });
});
