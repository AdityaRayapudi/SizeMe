function injectSizeButton() {
  const targetTexts = ['Sizes', 'Select Size', 'Choose Size', 'Size Options', 'Size Guide'];
  const productContainers = document.querySelectorAll('div, section, form');
  let sizeElement = null;

  // Find the size element on the page
  for (const container of productContainers) {
    const elements = container.querySelectorAll('*');
    for (const element of elements) {
      const elementText = element.textContent.trim().toLowerCase();
      if (targetTexts.some(targetText => elementText === targetText.toLowerCase())) {
        sizeElement = element;
        break;
      }
    }
    if (sizeElement) break;
  }

  if (sizeElement) {
    // Create the "FitMe" button
    const button = document.createElement('button');
    button.innerText = 'FitMe';
    button.style.margin = '10px';
    button.style.padding = '10px 20px';
    button.style.backgroundColor = 'black';
    button.style.color = '#fff';
    button.style.border = 'none';
    button.style.borderRadius = '5px';
    button.style.cursor = 'pointer';

    // Create the modal window (overlay content)
    const modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.top = '50%';
    modal.style.left = '50%';
    modal.style.transform = 'translate(-50%, -50%)';
    modal.style.backgroundColor = '#fff';
    modal.style.padding = '20px';
    modal.style.borderRadius = '10px';
    modal.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
    modal.style.zIndex = '1000';
    modal.style.display = 'none'; // Hidden initially

    // Create the iframe to load the external website
    const iframe = document.createElement('iframe');
    iframe.src = "http://127.0.0.1:5000";  // Replace with the URL of your hosted website
    iframe.style.width = '100%';
    iframe.style.height = '400px';  // You can adjust the height and width as needed
    iframe.style.border = 'none';

    // Add iframe to modal
    modal.appendChild(iframe);

    // Add the modal to the body
    document.body.appendChild(modal);

    // Create a background overlay for the modal
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    overlay.style.zIndex = '999'; // Just below the modal
    overlay.style.display = 'none'; // Hidden initially

    // Add overlay to body
    document.body.appendChild(overlay);

    // Show the modal and overlay when the button is clicked
    button.addEventListener('click', () => {
      modal.style.display = 'block'; // Show modal
      overlay.style.display = 'block'; // Show overlay
    });

    // Close modal when the close button is clicked
    document.getElementById('closeModalBtn')?.addEventListener('click', () => {
      modal.style.display = 'none';
      overlay.style.display = 'none'; // Hide overlay
    });

    // Hide modal and overlay if the user clicks outside the modal
    overlay.addEventListener('click', () => {
      modal.style.display = 'none';
      overlay.style.display = 'none'; // Hide overlay
    });

    // Add the button after the size element
    sizeElement.insertAdjacentElement('afterend', button);
  } else {
    console.error('Size element not found');
  }
}

injectSizeButton();
