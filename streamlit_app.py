import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="검 강화하기", page_icon="⚔️", layout="wide")

# 제목
st.title("⚔️ 검 강화하기")
st.write("확률과 조건부확률을 배워보자!")

# 검 이름 매핑
sword_names = {
    0: "나뭇잎 검",
    1: "검 모양 사탕",
    2: "낡은 단검",
    3: "화염의 검",
    4: "선택받은 마검",
    5: "형광검",
    6: "성스러운 검",
    7: "이도류",
    8: "샤이니 소드",
    9: "삼도류",
    10: "엑스칼리버",
}

def get_sword_name(level):
    return sword_names.get(level, "알 수 없는 검")

# 세션 상태 초기화
if 'sword_level' not in st.session_state:
    st.session_state.sword_level = 0
    st.session_state.total_attempts = 0
    st.session_state.total_successes = 0
    st.session_state.message = ""
    st.session_state.message_type = ""

# 강화 함수
def reinforce_sword():
    current_level = st.session_state.sword_level
    
    # 강화 확률 계산: 100% - (현재 레벨 * 10%)
    success_rate = max(0, 100 - (current_level * 10))
    
    # 확률에 따라 성공/실패 판정
    random_value = random.uniform(0, 100)
    is_success = random_value < success_rate
    
    # 상태 업데이트
    st.session_state.total_attempts += 1
    
    if is_success:
        st.session_state.sword_level += 1
        st.session_state.total_successes += 1
        st.session_state.message = "✅ 강화에 성공하였습니다!"
        st.session_state.message_type = "success"
    else:
        st.session_state.sword_level = 0
        st.session_state.message = "❌ 강화에 실패하였습니다.."
        st.session_state.message_type = "error"

# 초기화 함수
def reset_game():
    st.session_state.sword_level = 0
    st.session_state.total_attempts = 0
    st.session_state.total_successes = 0
    st.session_state.message = ""
    st.session_state.message_type = ""

# 탭 생성
tab1, tab2 = st.tabs(["🎮 게임", "📚 조건부확률 학습"])

# ========== 탭 1: 게임 ==========
with tab1:
    st.divider()
    current_level = st.session_state.sword_level
    success_rate = max(0, 100 - (current_level * 10))
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("현재 강화 레벨", f"+{current_level}")
    with col2:
        st.metric("현재 검", get_sword_name(current_level))
    with col3:
        st.metric("강화 성공률", f"{success_rate}%")

    # 강화 버튼
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        current_level = st.session_state.sword_level
        success_rate = max(0, 100 - (current_level * 10))
        is_disabled = success_rate == 0
        
        if st.button("⚔️ 강화하기", use_container_width=True, key="reinforce_btn", disabled=is_disabled):
            reinforce_sword()

    with col2:
        if st.button("🔄 초기화", use_container_width=True, key="reset_btn"):
            reset_game()
    
    if is_disabled:
        st.warning("🎉 축하합니다! +10 레벨 달성! 더 이상 강화할 수 없습니다.")

    # 메시지 표시
    if st.session_state.message:
        if st.session_state.message_type == "success":
            st.success(st.session_state.message)
        elif st.session_state.message_type == "error":
            st.error(st.session_state.message)
        elif st.session_state.message_type == "warning":
            st.warning(st.session_state.message)

    # 통계 정보
    st.divider()
    st.subheader("📊 통계")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("총 시도 횟수", st.session_state.total_attempts)
    with col2:
        st.metric("성공 횟수", st.session_state.total_successes)
    with col3:
        if st.session_state.total_attempts > 0:
            actual_success_rate = (st.session_state.total_successes / st.session_state.total_attempts) * 100
            st.metric("실제 성공률", f"{actual_success_rate:.1f}%")
        else:
            st.metric("실제 성공률", "0%")

    # 설명
    st.divider()
    st.subheader("📚 게임 규칙")
    st.write("""
    - **기본 강화 레벨**: +0 (강화 확률 100%)
    - **강화 메커니즘**: 강화 레벨이 +1씩 증가할 때마다 성공 확률이 10%씩 감소합니다.
    - **확률 공식**: 성공 확률(%) = 100 - (현재 레벨 × 10)
    - **실패 시**: 강화에 실패하면 검의 레벨이 다시 +0으로 초기화됩니다.
    - **최대 강화**: +10 레벨까지 강화 가능합니다 (강화 확률 0%).

    현재 검 목록:
    - +0 : 나뭇잎 검
    - +1 : 검 모양 사탕
    - +2 : 낡은 단검
    - +3 : 화염의 검
    - +4 : 선택받은 마검
    - +5 : 형광검
    - +6 : 성스러운 검
    - +7 : 이도류
    - +8 : 샤이니 소드
    - +9 : 삼도류
    - +10 : 엑스칼리버

    예시:
    - +0 → 강화 확률: 100%
    - +1 → 강화 확률: 90%
    - +2 → 강화 확률: 80%
    - +3 → 강화 확률: 70%
    - +10 → 강화 확률: 0%
    """)

# ========== 탭 2: 조건부확률 학습 ==========
with tab2:
    st.subheader("🧮 조건부확률 이해하기")
    
    st.write("""
    ### 조건부확률이란?
    **조건부확률**은 어떤 사건 A가 이미 일어났다는 것을 알 때, 그 조건 하에서 다른 사건 B가 일어날 확률입니다.
    
    수식: **P(B|A) = P(A ∩ B) / P(A)**
    
    더 쉽게 말하면, "A라는 상황이 주어졌을 때, B가 일어날 확률은 얼마인가?"를 나타냅니다.
    
    **예시:**
    - 날씨가 흐린 상태(A)일 때, 비가 올 확률(B) → P(비 | 흐림)
    - 검이 +3 레벨(A)에 있을 때, +4로 강화될 확률(B) → P(+4 달성 | +3 레벨)
    """)
    
    st.divider()
    
    st.write("""
    ### 검 강화 게임에서의 조건부확률
    
    **현재 레벨이 +3일 때를 생각해봅시다:**
    - 검이 지금 +3 레벨이라는 **조건** 하에서, 다음 강화에 성공할 확률은 70%입니다.
    - 만약 그 강화에 성공하여 +4가 되었다면, 이제 그 **새로운 조건** 하에서 +5로 강화될 확률은 60%입니다.
    
    **조건부확률 표기:**
    - P(+4 달성 | 현재 +3) = 70% ("현재 +3이라는 조건 하에서 +4에 달성할 확률")
    - P(+5 달성 | 현재 +4) = 60% ("현재 +4라는 조건 하에서 +5에 달성할 확률")
    
    **핵심 개념:** 조건부확률은 현재 상황(조건)이 주어졌을 때 다음에 일어날 가능성을 나타냅니다.
    """)
    
    st.divider()
    
    st.subheader("🎯 조건부 확률로 분석해보기")
    st.write("""
    ### 조건부 확률 활용: 특정 레벨에서 출발하여 목표 레벨 달성하기
    
    검을 한 번에 여러 레벨 강화해야 한다고 생각해봅시다. 예를 들어, 현재 +3에서 +10까지 도달해야 한다면?
    
    **단계별 조건부확률:**
    1. 지금 +3이라는 조건에서 → +4로 강화할 확률: 70%
    2. (만약 성공했다면) 이제 +4라는 새로운 조건에서 → +5로 강화할 확률: 60%  
    3. (계속 성공한다면) 이제 +5라는 조건에서 → +6으로 강화할 확률: 50%
    4. ... (이런 식으로 계속)
    
    **최종 확률 구하기:**
    각 단계에서의 조건부확률들을 모두 함께 고려했을 때, 지금 +3에서 출발하여 +10에 도달할 전체 확률은?
    
    = 70% × 60% × 50% × ... (각 단계의 조건부확률을 모두 곱함)
    """)
    
    st.divider()
    
    # 조건부 확률 분석을 위한 슬라이더
    st.write("**🎯 조건부 확률 계산 (특정 레벨에서 출발하는 경우)**")
    
    col1, col2 = st.columns(2)
    with col1:
        current_level_analysis = st.slider("현재 레벨 (조건)", 0, 9, 3, key="current_level_analysis")
    with col2:
        min_target = current_level_analysis + 1
        if min_target < 10:
            target_level_analysis = st.slider("목표 레벨 (이상)", min_target, 10, 10, key="target_level_analysis")
        else:
            st.write("목표 레벨: +10")
            target_level_analysis = 10
    
    # 조건부 확률 계산
    conditional_prob = 1.0
    for lv in range(current_level_analysis, target_level_analysis):
        success_rate = max(0, 100 - (lv * 10))
        conditional_prob *= (success_rate / 100)
    
    conditional_prob_percent = conditional_prob * 100
    
    # 계산 과정 표시
    prob_steps_conditional = []
    prob_values = []
    for lv in range(current_level_analysis, target_level_analysis):
        success_rate = max(0, 100 - (lv * 10))
        prob_steps_conditional.append(f"P(+{lv+1} | +{lv})")
        prob_values.append(f"{success_rate}%")
    
    st.write(f"**계산 과정:**")
    if prob_steps_conditional:
        # 곱셈정리를 이용한 설명
        st.write(f"**P(+{target_level_analysis} 도달 | 현재 +{current_level_analysis})**")
        
        st.write("**확률의 곱셈정리를 이용한 계산:**")
        st.write("현재 +{} 레벨에서 출발하여 각 단계를 모두 성공할 확률:".format(current_level_analysis))
        
        # 단계별 설명
        step_explanation = []
        for idx, lv in enumerate(range(current_level_analysis, target_level_analysis)):
            success_rate = max(0, 100 - (lv * 10))
            if idx == 0:
                step_explanation.append(f"1단계) 현재 +{lv}에서 +{lv+1}로 강화: {success_rate}%")
            else:
                step_explanation.append(f"{idx+1}단계) +{lv}에서 +{lv+1}로 강화: {success_rate}%")
        
        for step in step_explanation:
            st.write(step)
        
        st.write("\n**곱셈정리에 의해, 모든 단계를 연속으로 성공할 확률:**")
        st.write("= " + " × ".join(prob_values))
    else:
        st.write(f"이미 +{current_level_analysis} 레벨에 있습니다.")
    
    st.metric("최종 확률 (모든 조건부확률을 함께 고려)", f"{conditional_prob_percent:.2f}%")
    
    if conditional_prob > 0:
        try:
            attempts_conditional = max(1, int(round(1/conditional_prob)))
            st.info(f"💡 현재 +{current_level_analysis}에서 +{target_level_analysis} 이상에 도달하려면 평균적으로 약 {attempts_conditional}번 시도하면 성공할 수 있습니다!")
        except Exception:
            st.info("💡 시도 횟수 계산 중 오류가 발생했습니다.")
    else:
        st.info("💡 해당 구간은 성공 확률이 0%이므로 달성 불가합니다!")
    
    # 연속 성공 확률과 비교
    st.divider()
    st.write("**📊 연속 성공 확률과의 비교**")
    st.write("""
    ### 여러 조건부확률을 함께 생각하기
    
    게임에서 강화는 한 번에 끝나지 않습니다. 여러 번 연속으로 도전해야 높은 레벨에 도달합니다.
    
    **현재 +3에서 +10을 목표로 할 때:**
    - P(+4 달성 | 현재 +3) × P(+5 달성 | 현재 +4) × ... × P(+10 달성 | 현재 +9)
    - = 70% × 60% × 50% × 40% × 30% × 20% × 10%
    - = 약 0.0504% (매우 낮은 확률!)
    
    각 단계에서의 조건부확률을 모두 함께 고려할 때, 모든 조건이 만족되어야만 최종 목표에 도달할 수 있습니다.
    
    **주요 개념:**
    - 각 단계마다 "현재 상황"이 달라집니다 (조건이 변함)
    - 새로운 상황에서는 새로운 조건부확률이 적용됩니다
    - 모든 단계를 성공하려면 각 단계의 조건부확률을 모두 함께 고려해야 합니다
    """)
