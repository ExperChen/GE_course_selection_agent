<template>
  <div class="course-detail">
    <div v-if="!viewedCourse && blocks.length === 0" class="empty-state">
      <h2>👈 请在左侧选择课程添加到您的课表</h2>
    </div>

    <template v-if="viewedCourse">
      <div class="info-card">
        <h2>{{ viewedCourse['Course Name'] }} ({{ viewedCourse.Code }})</h2>
        <div class="info-grid">
          <p><strong>领域:</strong> {{ viewedCourse['GE Field'] }}</p>
          <p><strong>学分:</strong> {{ viewedCourse.Credit }}</p>
          <p><strong>讲师:</strong> {{ viewedCourse.Lecturer }}</p>
          <p><strong>名额:</strong> {{ viewedCourse.Quota }} (已申请: {{ viewedCourse.Apply }})</p>
        </div>
        <p class="time-raw"><strong>时间与地点:</strong> {{ viewedCourse['Time & Venue'] }}</p>
      </div>
    </template>

    <div class="timetable-container" v-show="blocks.length > 0">
      <div class="timetable">
        <div class="tt-header">Time</div>
        <div class="tt-header" v-for="day in days" :key="day">{{ day }}</div>

        <template v-for="i in 14" :key="'grid-'+i">
          <div class="tt-time" :style="{ gridRow: i + 1, gridColumn: 1 }">
            {{ i + 7 }}:00
          </div>
          <div class="tt-cell" v-for="d in 5" :key="'cell-'+i+'-'+d" 
               :style="{ gridRow: i + 1, gridColumn: d + 1 }">
          </div>
        </template>

        <div 
          v-for="(block, idx) in blocks" 
          :key="'block-'+idx"
          class="course-block-wrapper"
          :style="{ gridColumn: block.dayCol, gridRow: '2 / span 14' }"
        >
          <div 
            class="course-block" 
            :class="{ 
              'is-conflict': block.isConflict, 
              'is-viewed': viewedCourse && viewedCourse.Code === block.courseCode 
            }"
            :style="{ top: block.top + 'px', height: block.height + 'px' }"
          >
            <div class="block-code">{{ block.courseCode }}</div>
            <div class="block-venue">{{ block.venue }}</div>
            <div class="block-time">{{ block.timeStr }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  viewedCourse: { type: Object, default: null },
  blocks: { type: Array, default: () => [] }
});

const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
</script>

<style scoped>
.course-detail { flex: 1; display: flex; flex-direction: column; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); overflow: hidden; }
.empty-state { display: flex; align-items: center; justify-content: center; height: 100%; color: #888; flex: 1; }
.info-card { background: #f8f9fa; padding: 15px; border-radius: 6px; margin-bottom: 20px; flex-shrink: 0;}
.info-card h2 { margin: 0 0 10px 0; color: #0066cc; }
.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.info-grid p { margin: 0; font-size: 14px; }
.time-raw { margin-top: 10px; font-size: 13px; color: #555; border-top: 1px dashed #ccc; padding-top: 10px; }

/* 课表网格样式 */
.timetable-container { flex: 1; overflow-y: auto; }
.timetable { 
  display: grid; 
  grid-template-columns: 60px repeat(5, minmax(100px, 1fr)); 
  grid-template-rows: 40px repeat(14, 60px); 
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
  overflow: hidden; pointer-events: auto;
  display: flex; flex-direction: column; justify-content: center;
  transition: all 0.2s;
  opacity: 0.9;
}

/* 如果是当前聚焦查看的课程，给予描边加强视觉 */
.course-block.is-viewed {
  z-index: 5;
  box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.4);
  opacity: 1;
}

/* 冲突课程标红及动效 */
.course-block.is-conflict {
  background-color: #ffe6e6; 
  border-left: 4px solid #ff4d4f; 
  color: #a8071a;
  z-index: 10;
  animation: pulse 1s infinite alternate;
}
@keyframes pulse {
  from { box-shadow: 0 0 0 0 rgba(255, 77, 79, 0.7); }
  to { box-shadow: 0 0 0 6px rgba(255, 77, 79, 0); }
}

.block-code { font-weight: bold; font-size: 11px; margin-bottom: 2px;}
.block-venue { font-weight: bold; }
.block-time { font-size: 11px; opacity: 0.8; }
</style>