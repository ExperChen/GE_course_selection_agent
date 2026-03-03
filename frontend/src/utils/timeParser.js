export function parseTimeVenue(timeString) {
  if (!timeString) return [];
  
  const daysMap = { "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7 };
  const startHour = 8; // 课表从早8点开始
  const segments = timeString.split('|');
  const regex = /(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s+([0-9.]+)(am|pm)-([0-9.]+)(am|pm)\(([^)]+)\)/;
  
  const blocks = [];

  segments.forEach(seg => {
    const match = seg.trim().match(regex);
    if (match) {
      const day = match[1];
      const startNum = parseFloat(match[2]);
      const startAmPm = match[3];
      const endNum = parseFloat(match[4]);
      const endAmPm = match[5];
      const venue = match[6];

      // 转换为24小时制计算时长和偏移
      let startTime24 = (startAmPm === 'pm' && startNum < 12) ? startNum + 12 : startNum;
      let endTime24 = (endAmPm === 'pm' && endNum < 12) ? endNum + 12 : endNum;
      // 处理类似 12.00am 的边缘情况
      if (startAmPm === 'am' && startNum === 12) startTime24 = 0;
      if (endAmPm === 'am' && endNum === 12) endTime24 = 0;

      const topOffset = (startTime24 - startHour) * 60;
      const height = (endTime24 - startTime24) * 60;

      blocks.push({
        dayCol: daysMap[day] + 1, // +1 是因为 Grid 的第1列是时间轴
        top: topOffset,
        height: height - 2, // 减2像素防止边框重叠
        venue: venue,
        timeStr: `${startNum}${startAmPm} - ${endNum}${endAmPm}`
      });
    }
  });

  return blocks;
}