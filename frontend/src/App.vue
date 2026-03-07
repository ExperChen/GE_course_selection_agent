<template>
  <div class="app-container">
    <div v-if="loading" class="loading">正在加载课程数据...</div>
    <template v-else>
      <CourseList 
        :courses="courses" 
        :addedCourses="addedCourses"
        :viewedCourse="viewedCourse"
        :hasConflict="hasConflict"
        @add="handleAddCourse"
        @remove="handleRemoveCourse"
        @view="handleViewCourse"
      />
      <CourseDetail 
        :viewedCourse="viewedCourse" 
        :blocks="timetableData.blocks"
      />
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import Papa from 'papaparse';
import CourseList from './components/CourseList.vue';
import CourseDetail from './components/CourseDetail.vue';
import { parseTimeVenue } from './utils/timeParser';

const courses = ref([]);
const addedCourses = ref([]);
const viewedCourse = ref(null); // 当前正在查看详细信息的课程
const loading = ref(true);

onMounted(() => {
  Papa.parse('/courses_table.csv', {
    download: true,
    header: true,
    skipEmptyLines: true,
    complete: (results) => {
      courses.value = results.data.filter(item => item.Code);
      loading.value = false;
    },
    error: (err) => {
      console.error("CSV加载失败:", err);
      loading.value = false;
    }
  });
});

// 计算所有已选课程的课表块，并检测是否发生冲突
const timetableData = computed(() => {
  const blocks = [];
  let conflict = false;

  addedCourses.value.forEach(course => {
    const courseBlocks = parseTimeVenue(course['Time & Venue']);
    courseBlocks.forEach(b => {
      blocks.push({
        ...b,
        courseCode: course.Code,
        isConflict: false // 初始化无冲突
      });
    });
  });

  // O(N^2) 冲突检测，如果两节课在同一天且时间有交集则判定冲突
  for (let i = 0; i < blocks.length; i++) {
    for (let j = i + 1; j < blocks.length; j++) {
      const b1 = blocks[i];
      const b2 = blocks[j];
      if (b1.dayCol === b2.dayCol) {
        // 判断两个块的 top 和 height 是否重叠
        if (b1.top < b2.top + b2.height && b1.top + b1.height > b2.top) {
          b1.isConflict = true;
          b2.isConflict = true;
          conflict = true;
        }
      }
    }
  }

  return { blocks, conflict };
});

const hasConflict = computed(() => timetableData.value.conflict);

// 监听冲突变化，提示用户
watch(hasConflict, (newVal) => {
  if (newVal) {
    setTimeout(() => {
      alert('⚠️ 警告：课程时间发生冲突！请在左下角“已选课程”中删除冲突的课程。');
    }, 50); // 略微延时以保证DOM先渲染出红色块
  }
});

const handleAddCourse = (course) => {
  if (hasConflict.value) return; // 有冲突时锁定，禁止继续添加
  if (!addedCourses.value.find(c => c.Code === course.Code)) {
    addedCourses.value.push(course);
  }
  viewedCourse.value = course;
};

const handleRemoveCourse = (course) => {
  addedCourses.value = addedCourses.value.filter(c => c.Code !== course.Code);
  if (viewedCourse.value?.Code === course.Code) {
    // 删除了当前查看的课程时，将查看项切换为最后一个
    viewedCourse.value = addedCourses.value[addedCourses.value.length - 1] || null;
  }
};

const handleViewCourse = (course) => {
  viewedCourse.value = course;
};
</script>

<style>
body { margin: 0; background-color: #f5f7fa; font-family: sans-serif; }
.app-container { display: flex; gap: 20px; padding: 20px; height: 100vh; box-sizing: border-box; }
.loading { width: 100%; text-align: center; margin-top: 50px; font-size: 18px; color: #666; }
</style>