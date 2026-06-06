import streamlit as st
import random
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="검 강화하기", page_icon="⚔️", layout="wide")

# 제목
st.title("⚔️ 검 강화하기")
st.write("확률과 조건부확률을 배워보자!")

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
    col1, col2 = st.columns(2)
    with col1:
        st.metric("현재 강화 레벨", f"+{st.session_state.sword_level}")
    with col2:
        current_level = st.session_state.sword_level
        success_rate = max(0, 100 - (current_level * 10))
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
    **조건부확률**은 어떤 사건 A가 일어났을 때, 사건 B가 일어날 확률입니다.
    
    수식: **P(B|A) = P(A ∩ B) / P(A)**
    
    즉, "A가 발생했다는 조건 하에서 B가 발생할 확률"입니다.
    """)
    
    st.divider()
    
    st.write("""
    ### 검 강화 게임에서의 조건부확률
    
    **현재 레벨이 +3일 때를 생각해봅시다:**
    - 현재 강화 성공률: 70%
    - 만약 강화에 성공한다면, 다음 레벨(+4)에서의 강화 성공률은 60%입니다.
    
    **조건부확률 예시:**
    - P(+4 달성) = P(현재 +3에서 강화 성공) = 70%
    - P(+5 달성 | +4 달성) = 60% ("+4에 도달했다는 조건 하에서 +5에 도달할 확률")
    """)
    
    st.divider()
    
    st.subheader("� 연속 성공 확률 계산")
    st.write("""
    **먼저 특정 레벨과 목표 레벨을 정해두고, 배운 내용을 바탕으로 조건부확률이 어떻게 나올지 스스로 계산해보세요!**
    """)
    
    start_level = st.slider("시작 레벨", 0, 9, 0, key="start_level")
    end_level = st.slider("목표 레벨", start_level + 1, 10, 10, key="end_level")
    
    # 연속 성공 확률 계산
    continuous_success_prob = 1.0
    for lv in range(start_level, end_level):
        success_rate = max(0, 100 - (lv * 10))
        continuous_success_prob *= (success_rate / 100)
    
    continuous_success_percent = continuous_success_prob * 100
    
    st.write(f"""
    **+{start_level}에서 +{end_level}까지 모두 성공할 확률:**
    """)
    
    # 계산 과정 표시
    prob_steps = []
    for lv in range(start_level, end_level):
        success_rate = max(0, 100 - (lv * 10))
        prob_steps.append(f"P(+{lv}→+{lv+1}) = {success_rate}%")
    
    st.write(" × ".join(prob_steps))
    
    st.metric("전체 연속 성공 확률", f"{continuous_success_percent:.2f}%")
    
    if continuous_success_percent > 0:
        st.info(f"💡 평균적으로 약 {1/continuous_success_prob:.0f}번 시도하면 성공할 수 있습니다!")
    
    st.divider()
    
    st.subheader("🎯 학습 포인트")
    st.write("""
    1. **곱셈 법칙**: 여러 사건이 연속으로 일어날 확률은 각 확률을 곱합니다.
       - P(A ∩ B) = P(A) × P(B|A)
    
    2. **확률 감소**: 레벨이 올라갈수록 성공 확률이 감소하므로, 높은 레벨에 도달하기는 점점 어려워집니다.
    
    3. **기댓값**: 특정 레벨 달성에 필요한 평균 시도 횟수는 1을 연속 성공 확률로 나눈 값입니다.
    
    4. **조건부확률의 중요성**: 이전 시도의 결과가 다음 시도의 확률에 영향을 미칩니다.
    """)
