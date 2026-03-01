<template>
  <div class="app-container">
    <div v-if="loading" class="loading">正在加载课程数据...</div>
    <template v-else>
      <CourseList 
        :courses="courses" 
        :selectedCourse="selectedCourse"
        @select="handleSelectCourse" 
      />
      <CourseDetail :course="selectedCourse" />
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Papa from 'papaparse';
import CourseList from './components/CourseList.vue';
import CourseDetail from './components/CourseDetail.vue';

const courses = ref([]);
const selectedCourse = ref(null);
const loading = ref(true);

onMounted(() => {
  // 使用 PapaParse 读取 public 目录下的 CSV 文件
  Papa.parse('/courses_table.csv', {
    download: true,
    header: true,      // 自动将第一行作为对象的 key
    skipEmptyLines: true,
    complete: (results) => {
      // 整理数据，过滤掉没有 Code 的无效行
      courses.value = results.data.filter(item => item.Code);
      loading.value = false;
    },
    error: (err) => {
      console.error("CSV加载失败:", err);
      loading.value = false;
    }
  });
});

const handleSelectCourse = (course) => {
  selectedCourse.value = course;
};
</script>

<style>
body { margin: 0; background-color: #f5f7fa; font-family: sans-serif; }
.app-container { display: flex; gap: 20px; padding: 20px; height: 100vh; box-sizing: border-box; }
.loading { width: 100%; text-align: center; margin-top: 50px; font-size: 18px; color: #666; }
</style>