<template>
  <div class="about">
    <h1>About Outdoor Tracker</h1>
    <p>
      <strong>GitHub Repository:</strong>
      <a href="https://github.com/htschan/outdoortracker" target="_blank" rel="noopener">https://github.com/htschan/outdoortracker</a>
    </p>
    <p>
      <strong>Build Time:</strong> {{ buildTime }}
    </p>
    <p>
      <strong>GitHub SHA:</strong> {{ gitSha }}
    </p>
  </div>
</template>

<script setup>
const buildTime = import.meta.env.VITE_BUILD_TIME || 'unknown';
const gitSha = import.meta.env.VITE_GIT_SHA || 'unknown';
</script>

<style scoped>
.about {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.about h1 {
  margin-bottom: 1rem;
}
.about p {
  margin: 0.5rem 0;
}
</style>
