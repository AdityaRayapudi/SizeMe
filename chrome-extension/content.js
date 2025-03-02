function injectSizeButton() {
   
    const targetTexts = ['Sizes', 'Select Size', 'Choose Size', 'Size Options', 'Size Guide'];
  

    const productContainers = document.querySelectorAll('div, section, form');
    let sizeElement = null;
  
    
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
   
      const button = document.createElement('button');
      button.innerText = 'FitMe';
      button.style.margin = '10px';
      button.style.padding = '10px 20px';
      button.style.backgroundColor = 'black';
      button.style.color = '#fff';
      button.style.border = 'none';
      button.style.borderRadius = '5px';
      button.style.cursor = 'pointer';
  
     
      const popup = document.createElement('div');
      popup.style.position = 'fixed';
      popup.style.top = '50%';
      popup.style.left = '50%';
      popup.style.transform = 'translate(-50%, -50%)';
      popup.style.backgroundColor = '#fff';
      popup.style.padding = '20px';
      popup.style.borderRadius = '10px';
      popup.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
      popup.style.zIndex = '1000';
      popup.style.display = 'none'; 
  
      
      popup.innerHTML = `
       put FitMeContentHere
      `;
  
      document.body.appendChild(popup);
  
     
      button.addEventListener('click', () => {
        popup.style.display = 'block';
      });
  
  

      // inset size
      sizeElement.insertAdjacentElement('afterend', button);
    } else {
      console.error('nothing found');
    }
  }
  
  
  injectSizeButton();