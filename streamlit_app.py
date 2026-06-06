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
    **조건부확률**은 특정 조건이 주어진 상황에서 어떤 사건이 일어날 가능성을 나타내는 확률입니다.
    
    수식: **P(B|A) = P(A ∩ B) / P(A)**
    
    더 쉽게 말하면, "A라는 조건이 주어졌을 때, B의 가능성은 얼마인가?"를 나타냅니다.
    

    
    **예시:**
    - 하늘이 흐린 상태(조건)에서 비가 올 확률 → P(비 | 흐린 하늘)
    - 검이 +3 레벨(조건)일 때, 강화의 성공 확률 → P(강화 성공 | 검 레벨 +3)
    """)
    
    st.divider()
    
    st.write("""
    ### 검 강화 게임에서의 조건부확률
    
    검의 레벨에 따라 강화 성공 확률이 정해져 있습니다. 이는 게임의 규칙입니다.
    
    **게임의 규칙:**
    - 검의 레벨이 +3(조건)일 때, 강화 성공 확률: 70%
    - 검의 레벨이 +4(조건)일 때, 강화 성공 확률: 60%
    - 검의 레벨이 +5(조건)일 때, 강화 성공 확률: 50%
    
    **조건부확률 표기:**
    - P(강화 성공 | 검 레벨 +3) = 70%
    - P(강화 성공 | 검 레벨 +4) = 60%
    - P(강화 성공 | 검 레벨 +5) = 50%
    
    **핵심 개념:** 검의 레벨이라는 조건에 따라 강화 성공의 가능성이 달라집니다.
    """)
    
    st.divider()
    
    st.subheader("🎯 조건부 확률로 분석해보기")
    st.write("""
    ### 조건부 확률 활용: 여러 조건이 함께 만족되는 상황 분석하기
    
    게임에서 서로 다른 여러 조건들이 함께 고려되는 상황을 분석해봅시다. 예를 들어, 검이 +3부터 +10까지의 여러 레벨일 수 있는 상황을 생각해봅시다.
    
    **각 레벨에서의 강화 성공 확률 (조건에 따른 규칙):**
    - P(강화 성공 | 검 레벨 +3) = 70%
    - P(강화 성공 | 검 레벨 +4) = 60%
    - P(강화 성공 | 검 레벨 +5) = 50%
    - ... (계속)
    
    **여러 조건의 조합:**
    검이 동시에 +3 레벨이면서 AND 강화에 성공한다는 것은 무엇을 의미할까요?
    검이 동시에 +4 레벨이면서 AND 강화에 성공한다는 것은?
    
    이렇게 여러 조건들이 함께 일어나는 경우의 전체 가능성을 분석할 수 있습니다.
    """)
    
    st.divider()
    
    # 조건부 확률 분석을 위한 슬라이더
    st.write("**🎯 조건부 확률 계산**")
    
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
        st.write(f"**조건이 +{current_level_analysis}부터 +{target_level_analysis-1}까지일 때, 각 조건에서의 강화 성공 확률:**")
        
        st.write("**확률의 곱셈정리를 이용한 계산:**")
        st.write("다음 모든 조건이 함께 만족되는 경우의 확률:")
        
        # 조건별 설명
        condition_explanation = []
        for lv in enumerate(range(current_level_analysis, target_level_analysis)):
            lv = lv[1]
            success_rate = max(0, 100 - (lv * 10))
            condition_explanation.append(f"검 레벨이 +{lv}(조건)일 때, 강화 성공 확률: P(성공 | +{lv}) = {success_rate}%")
        
        for condition in condition_explanation:
            st.write(condition)
        
        st.write("\n**곱셈정리에 의해, 위의 모든 조건이 함께 만족되는 경우의 확률:**")
        st.write("= " + " × ".join(prob_values))
    else:
        st.write(f"이미 +{current_level_analysis} 레벨에 있습니다.")
    
    st.metric("최종 확률 (모든 조건이 함께 만족되는 경우)", f"{conditional_prob_percent:.2f}%")
    
    if conditional_prob > 0:
        try:
            attempts_conditional = max(1, int(round(1/conditional_prob)))
            st.info(f"💡 +{current_level_analysis}부터 +{target_level_analysis-1}까지의 모든 조건에서 강화에 성공할 경우의 수는 약 1/{int(1/conditional_prob)} 정도입니다.")
        except Exception:
            st.info("💡 확률 계산 중 오류가 발생했습니다.")
    else:
        st.info("💡 해당 구간은 성공 확률이 0%이므로 달성 불가합니다!")
    
    # 연속 성공 확률과 비교
    st.divider()
    st.write("**📊 연속 성공 확률과의 비교**")
    st.write("""
    ### 여러 조건부확률을 함께 고려하기
    
    게임 규칙에서 각 레벨마다 강화 성공 확률이 정해져 있습니다. 만약 우리가 알고 싶은 것이 다음과 같다면?
    
    **상황:** "검이 현재 +3, +4, +5, ..., +9 중 어느 레벨이든 있을 수 있을 때, 모두 강화에 성공할 가능성은?"
    
    **각 조건에서의 강화 성공 확률:**
    - P(성공 | 레벨 +3) = 70%
    - P(성공 | 레벨 +4) = 60%
    - P(성공 | 레벨 +5) = 50%
    - ... (계속)
    - P(성공 | 레벨 +9) = 10%
    
    **모든 조건이 함께 만족되는 경우의 확률:**
    
    "레벨 +3에서도 성공하고 AND 레벨 +4에서도 성공하고 AND ... AND 레벨 +9에서도 성공할" 전체 가능성은?
    
    확률의 곱셈정리에 의해:
    = 70% × 60% × 50% × 40% × 30% × 20% × 10%
    = 약 0.0504%
    
    **핵심:** 조건부확률을 함께 고려한다는 것은 모든 조건들이 동시에 만족되는 경우의 가능성을 계산하는 것입니다.
    """)
