<template>
  <div class="sidebar">
    <div class="course-list top-list" :class="{ 'disabled-list': hasConflict }">
      <h3 class="section-title">课程列表</h3>
      <div class="Search-Bar">
        <input
          placeholder="请输入查询课程"
          type="text"
          v-model="Search"
          class="search-input"
        /> 
      </div>
      <div class="list-content">
        <div 
          v-for="(course, index) in filteredCourses" 
          :key="index"
          class="course-item"
          @click="$emit('add', course)"
        >
          <div class="course-code">{{ course.Code }}</div>
          <div class="course-name">{{ course['Course Name'] }}</div>
        </div>
      </div>
    </div>

    <div class="course-list bottom-list">
      <h3 class="section-title">
        已选课程 
        <span v-if="hasConflict" class="conflict-text">(有冲突，请删除)</span>
      </h3>
      <div class="list-content">
        <div 
          v-for="(course, index) in addedCourses" 
          :key="'added-'+index"
          class="course-item added-item"
          :class="{ active: viewedCourse && viewedCourse.Code === course.Code }"
          @click="$emit('view', course)"
        >
          <div class="item-info">
            <div class="course-code">{{ course.Code }}</div>
            <div class="course-name">{{ course['Course Name'] }}</div>
          </div>
          <button class="delete-btn" @click.stop="$emit('remove', course)">删除</button>
        </div>
        <div v-if="addedCourses.length === 0" class="empty-hint">暂无已选课程</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  courses: { type: Array, required: true },
  addedCourses: { type: Array, default: () => [] },
  viewedCourse: { type: Object, default: null },
  hasConflict: { type: Boolean, default: false }
});
defineEmits(['add', 'remove', 'view']);

const Search = ref('');

const filteredCourses = computed(() => {
  const query = Search.value.trim().toLowerCase();
  if(!query){
    return props.courses;
  }
  return props.courses.filter(course => (
    course.Code.toLowerCase().includes(query) ||
    course['Course Name'].toLowerCase().includes(query)
  ));
});
</script>

<style scoped>
.sidebar {
  width: 300px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  height: 100%;
}
.course-list {
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
}
.top-list {
  flex: 1.5; /* 课程列表占更多高度 */
  overflow: hidden;
}
.bottom-list {
  flex: 0.75; /* 已选列表占较少高度 */
  overflow: hidden;
}
.section-title {
  margin-top: 0; margin-bottom: 12px; font-size: 16px; color: #333;
  display: flex; justify-content: space-between; align-items: center;
}
.conflict-text { color: #ff4d4f; font-size: 12px; font-weight: normal; }

.Search-Bar { margin-bottom: 15px; }
.search-input { width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }

.list-content { overflow-y: auto; flex: 1; padding-right: 5px; }
.course-item {
  padding: 12px; margin-bottom: 10px;
  border: 1px solid #e1e4e8; border-radius: 6px;
  cursor: pointer; transition: all 0.2s;
}
.course-item:hover { background-color: #f0f7ff; border-color: #0066cc; }
.course-item.active { background-color: #0066cc; color: white; border-color: #0066cc; }
.course-code { font-size: 12px; opacity: 0.8; }
.course-name { font-weight: bold; margin-top: 4px; }

/* 已选课程样式 */
.added-item { display: flex; justify-content: space-between; align-items: center; }
.item-info { flex: 1; }
.delete-btn {
  background-color: #ff4d4f; color: white;
  border: none; border-radius: 4px;
  padding: 6px 10px; cursor: pointer;
  font-size: 12px; margin-left: 10px; transition: background 0.2s;
}
.delete-btn:hover { background-color: #d9363e; }
.empty-hint { text-align: center; color: #999; font-size: 14px; margin-top: 20px; }

/* 冲突时的灰态限制样式 */
.disabled-list {
  opacity: 0.4;
  pointer-events: none;
  filter: grayscale(100%);
}
</style>