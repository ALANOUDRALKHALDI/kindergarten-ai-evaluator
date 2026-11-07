import streamlit as st
import google.generativeai as genai

# إعداد واجهة الصفحة
st.set_page_config(page_title="مساعد تقييم المعلمات", page_icon="🎓", layout="wide")

st.title("🎓 مساعد الذكاء الاصطناعي لتقييم أداء المعلمات والتطوير المهني")
st.markdown("يقوم هذا المساعد بتحليل درجات الزيارة الصفية والملاحظات واستخراج تقرير شامل وموضوعي لخطط التطوير.")

# شريط جانبي لإدخال مفتاح الـ API
st.sidebar.header("🔑 إعدادات الاتصال")
api_key_input = st.sidebar.text_input("أدخلي مفتاح Gemini API Key هنا:", type="password", value="AQ.Ab8RN6Lz6NL0sdMGxG6vT2febFX-7vLxnYyuV8R5za4fu0SO8g")

# نموذج إدخال البيانات
with st.form("eval_form"):
    st.subheader("📋 البيانات الأساسية")
    col1, col2 = st.columns(2)
    with col1:
        teacher_name = st.text_input("اسم المعلمة")
        visit_date = st.date_input("تاريخ الزيارة")
    with col2:
        stage = st.text_input("المستوى / الفصل", placeholder="مثال: المستوى الثاني / تمهيدي")

    st.subheader("📊 درجات المحاور (من 1 إلى 5)")
    c1, c2 = st.columns(2)
    with c1:
        score1 = st.slider("1. تهيئة بيئة التعلم وإدارة الصف", 1, 5, 3)
        score2 = st.slider("2. تنفيذ الأنشطة واستراتيجيات التدريس", 1, 5, 3)
    with c2:
        score3 = st.slider("3. مهارات التقويم والتشخيص ومتابعة نمو الطفل", 1, 5, 3)
        score4 = st.slider("4. التفاعل الوجداني والشراكة المجتمعية", 1, 5, 3)

    notes = st.text_area("📝 شواهد وملاحظات حرّة من الزيارة الصفية:")
    
    submit_btn = st.form_submit_button("🚀 تحليل وتقييم الأداء")

if submit_btn:
    if not api_key_input:
        st.error("⚠️ يرجى إدخال مفتاح Gemini API Key في الشريط الجانبي أولاً.")
    elif not teacher_name:
        st.warning("يرجى إدخال اسم المعلمة.")
    else:
        with st.spinner("جاري تحليل البيانات واستخراج التقرير..."):
            try:
                # إعداد الاتصال بالمفتاح والطريقة الكلاسيكية المستقرة
                genai.configure(api_key=api_key_input)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
أنت مستشار تربوي وخبير في تقييم أداء معلمات الطفولة المبكرة والاعتماد المهني.
قم بتحليل بيانات الزيارة الصفية التالية واستخراج تقرير احترافي:

- اسم المعلمة: {teacher_name}
- الفصل/المستوى: {stage}
- التاريخ: {visit_date}

[الدرجات]:
1. تهيئة بيئة التعلم وإدارة الصف: {score1}/5
2. تنفيذ الأنشطة واستراتيجيات التدريس: {score2}/5
3. مهارات التقويم والتشخيص: {score3}/5
4. التفاعل الوجداني والشراكة المجتمعية: {score4}/5

[الملاحظات المرصودة]:
{notes}

المطلوب تقديم تقرير منظم بالهيكل التالي:
1. ملخص الأداء العام (تحليل موضوعي وسردي).
2. أبرز نقاط القوة (الممارسات المتميزة التي حصلت على تقييم 4 أو 5).
3. مجالات التحسين ونقاط الضعف (المحاور التي حصلت على تقييم أقل بلغة تشجيعية).
4. خطة التطوير المهني الفردية المقترحة (IDP) (تتضمن أهدافاً تطويرية، أنشطة مقترحة كالورش أو الزيارات التبادلية، ومؤشر زمني).
"""
                response = model.generate_content(prompt)
                st.success("تم التقييم بنجاح!")
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
