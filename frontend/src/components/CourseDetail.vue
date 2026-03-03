<template>
  <div class="course-detail">
    <div v-if="!course" class="empty-state">
      <h2>👈 请在左侧选择一个课程查看详情</h2>
    </div>

    <template v-else>
      <div class="info-card">
        <h2>{{ course['Course Name'] }} ({{ course.Code }})</h2>
        <div class="info-grid">
          <p><strong>领域:</strong> {{ course['GE Field'] }}</p>
          <p><strong>学分:</strong> {{ course.Credit }}</p>
          <p><strong>讲师:</strong> {{ course.Lecturer }}</p>
          <p><strong>名额:</strong> {{ course.Quota }} (已申请: {{ course.Apply }})</p>
        </div>
        <p class="time-raw"><strong>时间与地点:</strong> {{ course['Time & Venue'] }}</p>
      </div>

      <div class="timetable-container">
        <div class="timetable">
          <div class="tt-header">Time</div>
          <div class="tt-header" v-for="day in days" :key="day">{{ day }}</div>

          <template v-for="i in 11" :key="'grid-'+i">
            <div class="tt-time" :style="{ gridRow: i + 1, gridColumn: 1 }">
              {{ i + 7 }}:00
            </div>
            <div class="tt-cell" v-for="d in 5" :key="'cell-'+i+'-'+d" 
                 :style="{ gridRow: i + 1, gridColumn: d + 1 }">
            </div>
          </template>

          <div 
            v-for="(block, idx) in courseBlocks" 
            :key="'block-'+idx"
            class="course-block-wrapper"
            :style="{ gridColumn: block.dayCol, gridRow: '2 / span 11' }"
          >
            <div class="course-block" :style="{ top: block.top + 'px', height: block.height + 'px' }">
              <div class="block-venue">{{ block.venue }}</div>
              <div class="block-time">{{ block.timeStr }}</div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { parseTimeVenue } from '../utils/timeParser';

const props = defineProps({
  course: { type: Object, default: null }
});

const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];

// 使用计算属性，当选中的 course 变化时，自动重新计算课表方块的数据
const courseBlocks = computed(() => {
  if (!props.course || !props.course['Time & Venue']) return [];
  return parseTimeVenue(props.course['Time & Venue']);
});
</script>

<style scoped>
.course-detail { flex: 1; display: flex; flex-direction: column; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); overflow: hidden; }
.empty-state { display: flex; align-items: center; justify-content: center; height: 100%; color: #888; }
.info-card { background: #f8f9fa; padding: 15px; border-radius: 6px; margin-bottom: 20px; flex-shrink: 0;}
.info-card h2 { margin: 0 0 10px 0; color: #0066cc; }
.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.info-grid p { margin: 0; font-size: 14px; }
.time-raw { margin-top: 10px; font-size: 13px; color: #555; border-top: 1px dashed #ccc; padding-top: 10px; }

/* 课表网格样式 */
.timetable-container { flex: 1; overflow-y: auto; }
.timetable { 
  display: grid; 
  grid-template-columns: 60px repeat(5, 1fr); 
  grid-template-rows: 40px repeat(11, 60px); 
  border-top: 1px solid #eee; border-left: 1px solid #eee; 
}
.tt-header { background: #fafafa; font-weight: bold; text-align: center; line-height: 40px; border-right: 1px solid #eee; border-bottom: 1px solid #eee; position: sticky; top: 0; z-index: 10;}
.tt-time { text-align: right; padding-right: 10px; font-size: 12px; color: #888; border-right: 1px solid #eee; border-bottom: 1px solid #eee; padding-top: 5px; }
.tt-cell { border-right: 1px solid #eee; border-bottom: 1px dashed #eee; }

/* 课程方块定位封装 */
.course-block-wrapper { position: relative; pointer-events: none; }
.course-block {
  position: absolute; left: 2px; right: 2px;
  background-color: #e1f0ff; border-left: 4px solid #0066cc; color: #004a99;
  border-radius: 4px; padding: 5px; font-size: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  overflow: hidden; z-index: 5; pointer-events: auto;
  display: flex; flex-direction: column; justify-content: center;
}
.block-venue { font-weight: bold; }
.block-time { font-size: 11px; opacity: 0.8; }
</style>