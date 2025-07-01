<script setup>
import { ref, onMounted } from "vue";

let url = `/api`;

const rows = ref([]);
const values = ref({});
const loading = ref(true);
const error = ref(null);

async function fetchValue(index) {
  try {
    const response = await fetch(index ? `${url}/values/${index}` : url);
    if (!response.ok) throw new Error("Network error");
    const jsonResponse = await response.json();

    if (!index) {
      rows.value = jsonResponse;
    } else {
      return parseInt(jsonResponse[0].Value);
    }
  } catch (err) {
    console.error("Error fetching data:", err);
    error.value = err.message;
    if (!index) rows.value = [];
  }
}

async function ArrangeValues() {
  try {
    const [A5, A20, A15, A7, A12, A13] = await Promise.all([
      fetchValue("A5"),
      fetchValue("A20"),
      fetchValue("A15"),
      fetchValue("A7"),
      fetchValue("A12"),
      fetchValue("A13"),
    ]);

    values.value = { A5, A20, A15, A7, A12, A13 };
  } catch (err) {
    error.value = "Failed to load calculation values";
  }
}

onMounted(async () => {
  await fetchValue();
  await ArrangeValues();
  loading.value = false;
});
</script>

<template>
  <div class="container">
    <div v-if="loading" class="loading">Loading data...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else class="tables-container">
      <div class="table-wrapper">
        <table class="table">
          <caption>
            Table 1
          </caption>
          <thead>
            <tr>
              <th>Index #</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in rows" :key="row.index">
              <td>{{ row.index }}</td>
              <td>{{ row.Value }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="table-wrapper">
        <table class="table">
          <caption>
            Table 2
          </caption>
          <thead>
            <tr>
              <th>Category</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Alpha</td>
              <td>{{ values.A5 + values.A20 }}</td>
            </tr>
            <tr>
              <td>Beta</td>
              <td>{{ values.A15 / values.A7 }}</td>
            </tr>
            <tr>
              <td>Charlie</td>
              <td>{{ values.A13 * values.A12 }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  font-family: "Segoe UI", Roboto, sans-serif;
}

.loading,
.error {
  padding: 1.5rem 2rem;
  border-radius: 8px;
  font-weight: 500;
  text-align: center;
}

.loading {
  background: rgba(59, 130, 246, 0.1);
  color: #1e40af;
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.error {
  background: rgba(239, 68, 68, 0.1);
  color: #dc2626;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.tables-container {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  justify-content: center;
  align-items: flex-start;
  max-width: 900px;
  width: 100%;
}

.table-wrapper {
  flex: 1;
  min-width: 300px;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.table-wrapper:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 16px -4px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table caption {
  padding: 1rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  background: #f9fafb;
  border-bottom: 2px solid #e5e7eb;
}

.table th {
  padding: 0.875rem 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  background: #f3f4f6;
  border-bottom: 1px solid #e5e7eb;
}

.table th:first-child {
  border-top-left-radius: 0;
}

.table th:last-child {
  border-top-right-radius: 0;
}

.table td {
  padding: 0.875rem 1rem;
  color: #6b7280;
  border-bottom: 1px solid #f3f4f6;
  transition: background-color 0.15s ease;
}

.table tbody tr:hover td {
  background: #f9fafb;
}

.table tbody tr:last-child td {
  border-bottom: none;
}

.table tbody tr:last-child td:first-child {
  border-bottom-left-radius: 12px;
}

.table tbody tr:last-child td:last-child {
  border-bottom-right-radius: 12px;
}

/* Responsive design */
@media (max-width: 768px) {
  .container {
    padding: 1rem;
  }

  .tables-container {
    flex-direction: column;
    width: 100%;
    gap: 1.5rem;
  }

  .table-wrapper {
    min-width: 100%;
  }

  .table th,
  .table td {
    padding: 0.75rem;
  }

  .table caption {
    padding: 0.75rem;
    font-size: 1.125rem;
  }
}
</style>
