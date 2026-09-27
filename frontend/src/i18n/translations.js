export const dateLocales = {
  th: 'th-TH-u-ca-gregory',
  en: 'en-GB',
}

export const translations = {
  th: {
    languageSelector: 'เลือกภาษา',
    dashboardTitle: 'แดชบอร์ดเหตุการณ์ผิดปกติ',
    dashboardDescription:
      'ตรวจสอบความผิดปกติ หลักฐาน และคำอธิบายที่สร้างโดย AI',
    apiConnected: 'เชื่อมต่อ API แล้ว',
    loadingData: 'กำลังโหลดข้อมูล',
    apiUnavailable: 'เชื่อมต่อ API ไม่ได้',
    loadingTitle: 'กำลังโหลดเหตุการณ์',
    loadingDescription:
      'กรุณารอสักครู่ ขณะที่ LogSense ดึงข้อมูลจาก API',
    errorTitle: 'โหลดข้อมูลไม่สำเร็จ',
    errorDescription:
      'ตรวจสอบว่า backend API กำลังทำงาน แล้วลองอีกครั้ง',
    retry: 'ลองใหม่',
    emptyTitle: 'ยังไม่พบเหตุการณ์ผิดปกติ',
    emptyDescription:
      'API ทำงานตามปกติ แต่ยังไม่มี incident ให้แสดง',
    monitoring: 'การเฝ้าระวัง',
    incidents: 'เหตุการณ์',
    selectedIncident: 'เหตุการณ์ที่เลือก',
    metricEvidence: 'หลักฐานจากเมตริก',
    requests: 'คำขอทั้งหมด',
    errors: 'ข้อผิดพลาด',
    errorRate: 'อัตราข้อผิดพลาด',
    p95Latency: 'เวลาแฝง P95',
    timeline: 'ลำดับเวลาของหลักฐาน',
    windowStart: 'เวลาเริ่มช่วง',
    anomalyReason: 'เหตุผลที่ตรวจพบ',
    geminiAnalysis: 'การวิเคราะห์โดย Gemini',
    evidenceBasedExplanation: 'คำอธิบายจากหลักฐาน',
    observedFacts: 'ข้อเท็จจริงที่พบ',
    likelyExplanation: 'คำอธิบายที่เป็นไปได้',
    uncertainty: 'ความไม่แน่นอน',
    recommendedNextChecks: 'สิ่งที่ควรตรวจสอบต่อ',
    detector: 'ตัวตรวจจับ',
    prompt: 'พรอมต์',
    evidenceRows: 'แถวหลักฐาน',
    analysisSourceNote:
      'เนื้อหาการวิเคราะห์ด้านล่างเป็นต้นฉบับภาษาอังกฤษ',
    severity: {
      low: 'ต่ำ',
      medium: 'ปานกลาง',
      high: 'สูง',
    },
    status: {
      open: 'กำลังตรวจสอบ',
      resolved: 'แก้ไขแล้ว',
    },
  },
  en: {
    languageSelector: 'Select language',
    dashboardTitle: 'Incident Dashboard',
    dashboardDescription:
      'Review detected anomalies, supporting evidence, and AI-generated explanations.',
    apiConnected: 'API connected',
    loadingData: 'Loading data',
    apiUnavailable: 'API unavailable',
    loadingTitle: 'Loading incidents',
    loadingDescription:
      'Please wait while LogSense fetches data from the API.',
    errorTitle: 'Unable to load incidents',
    errorDescription:
      'Check that the backend API is running, then try again.',
    retry: 'Try again',
    emptyTitle: 'No incidents detected',
    emptyDescription:
      'The API is available, but there are no incidents to display.',
    monitoring: 'Monitoring',
    incidents: 'Incidents',
    selectedIncident: 'Selected incident',
    metricEvidence: 'Metric evidence',
    requests: 'Requests',
    errors: 'Errors',
    errorRate: 'Error rate',
    p95Latency: 'P95 latency',
    timeline: 'Evidence timeline',
    windowStart: 'Window start',
    anomalyReason: 'Detection reason',
    geminiAnalysis: 'Gemini analysis',
    evidenceBasedExplanation: 'Evidence-based explanation',
    observedFacts: 'Observed facts',
    likelyExplanation: 'Likely explanation',
    uncertainty: 'Uncertainty',
    recommendedNextChecks: 'Recommended next checks',
    detector: 'Detector',
    prompt: 'Prompt',
    evidenceRows: 'Evidence rows',
    analysisSourceNote:
      'The analysis below is the canonical English response.',
    severity: {
      low: 'Low',
      medium: 'Medium',
      high: 'High',
    },
    status: {
      open: 'Open',
      resolved: 'Resolved',
    },
  },
}
