<template>
  <div class="course-list">
    <div 
      v-for="(course, index) in courses" 
      :key="index"
      class="course-item"
      :class="{ active: selectedCourse && selectedCourse.Code === course.Code && selectedCourse['Course Name'] === course['Course Name'] }"
      @click="$emit('select', course)"
    >
      <div class="course-code">{{ course.Code }}</div>
      <div class="course-name">{{ course['Course Name'] }}</div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  courses: { type: Array, required: true },
  selectedCourse: { type: Object, default: null }
});
defineEmits(['select']);
</script>

<style scoped>
.course-list {
  width: 300px;
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  overflow-y: auto;
}
.course-item {
  padding: 12px; margin-bottom: 10px;
  border: 1px solid #e1e4e8; border-radius: 6px;
  cursor: pointer; transition: all 0.2s;
}
.course-item:hover { background-color: #f0f7ff; border-color: #0066cc; }
.course-item.active { background-color: #0066cc; color: white; }
.course-code { font-size: 12px; opacity: 0.8; }
.course-name { font-weight: bold; margin-top: 4px; }
</style>