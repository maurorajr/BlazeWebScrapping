function toggleSubmenu(element) {
  const parent = element.parentElement;
  parent.classList.toggle('expanded');
}

async function loadContent(action) {
  const content = document.querySelector('.content');

  content.innerHTML = `<h1>Carregando...</h1>`;

  try {
      const response = await fetch(`/api/${action}`);
      if (response.ok) {
          const data = await response.json();
          content.innerHTML = `<h1>${data.title}</h1><p>${data.message}</p>`;

          if (data.details) {
              let tableHTML = `
                  <table border="1">
                      <thead>
                          <tr>
                              <th>Data</th>
                              <th>ID</th>
                              <th>Tipo</th>
                              <th>Quantia</th>
                              <th>Status</th>
                          </tr>
                      </thead>
                      <tbody>
              `;
              data.details.forEach(item => {
                  tableHTML += `
                      <tr>
                          <td>${item.date}</td>
                          <td>${item.id}</td>
                          <td>${item.type}</td>
                          <td>R$ ${item.amount.toFixed(2)}</td>
                          <td>${item.status}</td>
                      </tr>
                  `;
              });
              tableHTML += '</tbody></table>';
              content.innerHTML += tableHTML;
          }
      } else {
          content.innerHTML = `<h1>Erro</h1><p>Ocorreu um erro ao processar a ação.</p>`;
      }
  } catch (error) {
      content.innerHTML = `<h1>Erro</h1><p>${error.message}</p>`;
  }
}
