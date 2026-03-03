<template>
  <div class="course-list">
    <div class="Search-Bar">
      <input
        placeholder="请输入查询课程"
        type="text"
        v-model="Search"
        class="search-input"
      /> 
    </div>
    <div 
      v-for="(course, index) in filteredCourses" 
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
import { ref , computed} from 'vue';

const props = defineProps({
  courses: { type: Array, required: true },
  selectedCourse: { type: Object, default: null }
});
defineEmits(['select']);


const Search=ref('');

const filteredCourses=computed(()=>{

  const query=Search.value.trim();

  if(!query){
    return props.courses;
  }

  return props.courses.filter(course=>(
    course.Code.includes(query) ||
    course['Course Name'].includes(query)
  ));


});


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

.search-input{
  /* 你的样式保持不变，加一个搜索框样式 */

  width: 50%;
  padding: 8px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;

}

</style>