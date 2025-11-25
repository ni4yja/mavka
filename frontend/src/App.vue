<script setup>
import { ref } from 'vue'

const stats = ref(null)
const error = ref(null)
const loading = ref(false)
const selectedSource = ref(null)

async function loadStats() {
  loading.value = true
  stats.value = null
  error.value = null
  selectedSource.value = null

  try {
    const res = await fetch('http://localhost:8000/api/articles/stats')
    if (!res.ok)
      throw new Error(`HTTP ${res.status}`)
    stats.value = await res.json()
  }
  catch (err) {
    error.value = err.message
  }
  finally {
    loading.value = false
  }
}

function selectSource(source) {
  selectedSource.value = selectedSource.value === source ? null : source
}

function getSourceCount(source) {
  return stats.value?.by_source?.[source] || 0
}
</script>

<template>
  <div class="container">
    <h2>📊 Sources Statistics</h2>

    <button :disabled="loading" class="load-btn" @click="loadStats">
      {{ loading ? 'Loading...' : 'Load Statistics' }}
    </button>

    <!-- Error Message -->
    <p v-if="error" class="error">
      ❌ Error: {{ error }}
    </p>

    <!-- Statistics View -->
    <div v-if="stats" class="stats-container">
      <div class="total-info">
        <h3>Total Articles: <span class="count">{{ stats.total }}</span></h3>
      </div>

      <div v-if="stats.by_source && Object.keys(stats.by_source).length > 0" class="sources-list">
        <button
          v-for="(count, source) in stats.by_source"
          :key="source"
          class="source-btn" :class="[{ active: selectedSource === source }]"
          @click="selectSource(source)"
        >
          <span class="source-name">{{ source }}</span>
          <span class="source-count">{{ count }}</span>
        </button>
      </div>

      <!-- Selected Source Details -->
      <div v-if="selectedSource" class="selected-source">
        <h4>{{ selectedSource }}</h4>
        <p>Articles: <strong>{{ getSourceCount(selectedSource) }}</strong></p>
      </div>
    </div>

    <!-- No Data -->
    <p v-else-if="!loading && !error" class="no-data">
      Click "Load Statistics" to fetch data
    </p>
  </div>
</template>

<style scoped>
.container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

h2 {
  color: #333;
  margin-bottom: 20px;
}

.load-btn {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s;
}

.load-btn:hover:not(:disabled) {
  background: #45a049;
}

.load-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error {
  color: #d32f2f;
  background: #ffebee;
  padding: 10px;
  border-radius: 4px;
  margin-top: 10px;
}

.stats-container {
  margin-top: 20px;
}

.total-info {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.total-info h3 {
  margin: 0;
  font-size: 18px;
}

.count {
  color: #4CAF50;
  font-weight: bold;
  font-size: 24px;
}

.sources-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.source-btn {
  background: white;
  border: 2px solid #e0e0e0;
  padding: 12px 15px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s;
  font-size: 14px;
}

.source-btn:hover {
  border-color: #4CAF50;
  background: #f9f9f9;
}

.source-btn.active {
  background: #4CAF50;
  color: white;
  border-color: #4CAF50;
}

.source-name {
  font-weight: 500;
}

.source-count {
  background: rgba(0, 0, 0, 0.1);
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: bold;
  font-size: 12px;
}

.source-btn.active .source-count {
  background: rgba(255, 255, 255, 0.3);
}

.selected-source {
  margin-top: 20px;
  padding: 15px;
  background: #e8f5e9;
  border-left: 4px solid #4CAF50;
  border-radius: 4px;
}

.selected-source h4 {
  margin-top: 0;
  color: #2e7d32;
}

.no-data {
  color: #999;
  text-align: center;
  margin-top: 20px;
}
</style>
