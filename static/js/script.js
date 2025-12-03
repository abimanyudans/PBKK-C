const overviewProcessing = document.getElementById("overview-processing");
const overviewDesc = document.getElementById("overview-desc");
const successMsg = document.getElementById("success-message");
const overviewMetrics = document.getElementById("overview-metrics");
document.getElementById("csvFile").addEventListener("change", function (e) {
  if (!e.target.files.length) return;
  
  const file = e.target.files[0];
  const fileSize = (file.size / 1024 / 1024).toFixed(2); // Size in MB
  
  overviewProcessing.classList.add("active");
  overviewDesc.classList.add("hide");
  
  // Update processing text with file info
  const processingText = document.querySelector('.overview-text');
  processingText.textContent = `Processing ${file.name} (${fileSize} MB)... Please wait.`;
  
  console.log(`Processing CSV file: ${file.name} (${fileSize} MB)`);
  
  // Use web worker for large files (> 1MB) to avoid blocking UI
  const useWorker = file.size > 1024 * 1024;
  
  setTimeout(() => {
    Papa.parse(file, {
      header: true,
      dynamicTyping: true,
      skipEmptyLines: true,
      worker: useWorker, // Use web worker for large files
      complete: function (results) {
        try {
          const data = results.data;
          console.log(`CSV parsed successfully: ${data.length} rows`);
          
          // Try storing with progressively smaller datasets
          let stored = false;
          const maxRowsLevels = [5000, 3000, 1000, 500]; // Try different sizes
          
          for (let maxRows of maxRowsLevels) {
            try {
              const dataToStore = data.slice(0, maxRows);
              localStorage.setItem("creditcard_csv_data", JSON.stringify(dataToStore));
              console.log(`Successfully stored ${dataToStore.length} rows in localStorage`);
              
              if (data.length > maxRows) {
                console.warn(`File has ${data.length} rows. Stored ${maxRows} rows due to storage limits.`);
              }
              
              stored = true;
              break; // Success! Exit loop
            } catch (storageError) {
              console.warn(`Failed to store ${maxRows} rows, trying smaller dataset...`);
              continue; // Try next smaller size
            }
          }
          
          if (!stored) {
            console.error('Failed to store data in localStorage. Storage quota exceeded.');
            alert('Warning: Unable to save full dataset due to browser storage limits. Overview will still be displayed.');
          }
          
          showSuccessMessage();
          updateOverview(data); // Use full data for overview
          overviewProcessing.classList.remove("active");
        } catch (error) {
          console.error('Error processing CSV:', error);
          alert(`Error processing CSV file: ${error.message}\nPlease check the file format.`);
          overviewProcessing.classList.remove("active");
          overviewDesc.classList.remove("hide");
        }
      },
      error: function(error) {
        console.error('CSV parsing error:', error);
        alert('Error parsing CSV file: ' + error.message);
        overviewProcessing.classList.remove("active");
        overviewDesc.classList.remove("hide");
      }
    });
  }, 200);
});

function toggleSidebar() {
  document.querySelector(".sidebar").classList.toggle("active");
}

// Close sidebar when clicking outside
document.addEventListener("click", function (event) {
  const sidebar = document.querySelector(".sidebar");
  const menuToggle = document.querySelector(".menu-toggle");

  if (
    sidebar &&
    menuToggle &&
    !sidebar.contains(event.target) &&
    !menuToggle.contains(event.target) &&
    window.innerWidth <= 900
  ) {
    sidebar.classList.remove("active");
  }
});

// Handle window resize
window.addEventListener("resize", function () {
  const sidebar = document.querySelector(".sidebar");
  if (sidebar && window.innerWidth >= 900) {
    sidebar.classList.remove("active");
  }
});

function showSuccessMessage() {
  successMsg.style.display = "block";
  successMsg.textContent = "✅ Data uploaded and processed successfully!";
}

// Overview metrics
function updateOverview(data) {
  const total = data.length;
  const frauds = data.filter((row) => row["Class"] === 1).length;
  const legit = total - frauds;
  overviewMetrics.innerHTML = `
        <ul>
          <li><strong>Total Transactions:</strong> ${total}</li>
          <li><strong>Fraudulent Transactions:</strong> ${frauds}</li>
          <li><strong>Legitimate Transactions:</strong> ${legit}</li>
          <li><strong>Fraud Rate:</strong> ${((frauds / total) * 100).toFixed(
            4
          )}%</li>
        </ul>
      `;
}
