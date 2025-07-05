import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json
from collections import defaultdict
import pandas as pd

# Set page config
st.set_page_config(
    page_title="LeetCode: Minimum Area Rectangle",
    page_icon="📐",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .step-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .success-box {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
    }
    .warning-box {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎯 LeetCode: Minimum Area Rectangle</h1>
    <p>Interactive Learning Environment for Algorithm Mastery</p>
</div>
""", unsafe_allow_html=True)

# JavaScript implementation (for reference)
js_code = '''
/**
Before using this code, there is a note that the time limited
exceeded for this code but it was all fine thus i used it here
and chnaged my approach to use a different one
 * @param {number[][]} points
 * @return {number}
 */
var minAreaRect = function (points) {
    // let xCord = new Map();
    let yCord = new Map();
    let pointSet = new Set();

    // Store points in a set for fast lookup
    for (let [x, y] of points) {
        pointSet.add(`${x},${y}`);
    }

    // Y Coordinate (vertical lines)
    points.sort((a, b) => a[0] - b[0]);
    for (let i = 0; i < points.length; i++) {
        let difY;
        if (points[i][0] == points[i + 1]?.[0]) {
            difY = points[i + 1][1] - points[i][1];
            if (!yCord.has(difY)) {
                yCord.set(difY, []);
            }
            yCord.get(difY).push([points[i], points[i + 1]]);
        }
    }

    let minArea = Infinity;

    // Try all pairs of vertical lines
    for (let difY of yCord.keys()) {
        let verticalPairs = yCord.get(difY);
        for (let i = 0; i < verticalPairs.length; i++) {
            for (let j = i + 1; j < verticalPairs.length;) {
                let [[x1, ya1], [x1b, ya2]] = verticalPairs[i];
                let [[x2, yb1], [x2b, yb2]] = verticalPairs[j];
                // to keep the Y's in correct order that is y3 is smaller and y4 is greater

                let y1 = Math.min(ya1, ya2);
                let y2 = Math.max(ya1, ya2);
                let y3 = Math.min(yb1, yb2);
                let y4 = Math.max(yb1, yb2);

                // Check if horizontal segments can connect these two verticals
                if (
                    y1 === y3 && y2 === y4 && // matching y-positions
                    pointSet.has(`${x1},${y1}`) &&
                    pointSet.has(`${x1},${y2}`) &&
                    pointSet.has(`${x2},${y1}`) &&
                    pointSet.has(`${x2},${y2}`)
                ) {
                    let area = Math.abs(x1 - x2) * difY;
                    minArea = Math.min(minArea, area);
                }
            }
        }
    }

    return minArea === Infinity ? 0 : minArea;
};



'''

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

# Sidebar for navigation
st.sidebar.markdown("## Learning Dashboard")
st.sidebar.metric("Score", st.session_state.score)
st.sidebar.metric("Attempts", st.session_state.attempts)

# Main content
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📍 Problem Setup", 
    "🧠 Predict & Test", 
    "🔍 Algorithm Deep Dive", 
    "📊 Visual Analysis", 
    "🧪 Debug Mode"
])

# Python implementation of the algorithm
def min_area_rect(points):
    if len(points) < 4:
        return 0
    
    # Create a set for O(1) lookup
    point_set = set()
    for point in points:
        point_set.add(f"{point[0]},{point[1]}")
    
    # Group points by y-coordinate
    y_cord = defaultdict(list)
    for point in points:
        y = point[1]
        y_cord[y].append(point[0])
    
    min_area = float('inf')
    steps = []
    
    # Check all pairs of points with same y-coordinate
    for y, x_list in y_cord.items():
        if len(x_list) < 2:
            continue
        
        for i in range(len(x_list)):
            for j in range(i + 1, len(x_list)):
                x1, x2 = x_list[i], x_list[j]
                
                # Look for another horizontal line
                for y2, x_list2 in y_cord.items():
                    if y2 == y or len(x_list2) < 2:
                        continue
                    
                    # Check if both vertical lines exist
                    if f"{x1},{y2}" in point_set and f"{x2},{y2}" in point_set:
                        area = abs(x2 - x1) * abs(y2 - y)
                        steps.append({
                            'rectangle': [(x1, y), (x2, y), (x1, y2), (x2, y2)],
                            'area': area,
                            'width': abs(x2 - x1),
                            'height': abs(y2 - y)
                        })
                        min_area = min(min_area, area)
    
    return min_area if min_area != float('inf') else 0, steps

# Preset test cases
presets = {
    "Simple Rectangle": [[1,1],[1,3],[3,1],[3,3]],
    "Multiple Rectangles": [[1,1],[1,3],[3,1],[3,3],[0,1],[0,3],[2,1],[2,3]],
    "No Rectangle": [[1,1],[2,2],[3,3],[4,4]],
    "Single Point": [[1,1]],
    "Collinear Points": [[1,1],[2,1],[3,1],[4,1]],
    "Complex Case": [[1,1],[1,3],[3,1],[3,3],[2,2],[4,2],[2,4],[4,4]]
}

with tab1:
    st.markdown("## 📍 Problem Understanding")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Problem Statement")
        st.markdown("""
        Given a set of points in the xy-plane, determine the minimum area of a rectangle 
        formed from these points, with sides parallel to the x and y axes.
        
        **Key Constraints:**
        - Rectangle sides must be parallel to axes
        - All 4 corners must be from the given points
        - Return 0 if no rectangle can be formed
        """)
        
    
    with col2:
        st.markdown("### Choose Your Input")
        
        input_method = st.radio("How do you want to input points?", 
                               ["Use Preset", "Custom Input"])
        
        if input_method == "Use Preset":
            preset_name = st.selectbox("Choose a preset:", list(presets.keys()))
            points = presets[preset_name]
            st.write(f"**Selected:** {preset_name}")
            st.write(f"**Points:** {points}")
        else:
            st.markdown("Enter points as [[x1,y1],[x2,y2],...] format:")
            custom_input = st.text_area("Points:", value="[[1,1],[1,3],[3,1],[3,3]]")
            try:
                points = json.loads(custom_input)
                if not isinstance(points, list) or not all(isinstance(p, list) and len(p) == 2 for p in points):
                    st.error("Invalid format! Use [[x1,y1],[x2,y2],...] format")
                    points = [[1,1],[1,3],[3,1],[3,3]]
                else:
                    st.success(f"✅ Valid input with {len(points)} points")
            except:
                st.error("Invalid JSON format!")
                points = [[1,1],[1,3],[3,1],[3,3]]
        
        # Store points in session state
        st.session_state.points = points
    
    st.markdown("### JavaScript Implementation")
    st.code(js_code, language='javascript')

with tab2:
    st.markdown("## 🧠 Predict & Test Your Understanding")
    
    if 'points' not in st.session_state:
        st.warning("Please set up points in the Problem Setup tab first!")
    else:
        points = st.session_state.points
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Make Your Prediction")
            st.write(f"**Current Points:** {points}")
            
            # Visualization of points
            fig, ax = plt.subplots(figsize=(8, 6))
            if points:
                x_coords = [p[0] for p in points]
                y_coords = [p[1] for p in points]
                ax.scatter(x_coords, y_coords, c='red', s=100, alpha=0.7)
                
                for i, (x, y) in enumerate(points):
                    ax.annotate(f'({x},{y})', (x, y), xytext=(5, 5), 
                              textcoords='offset points', fontsize=9)
                
                ax.grid(True, alpha=0.3)
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_title('Points Visualization')
            
            st.pyplot(fig)
            
            st.markdown("**Think about it:**")
            st.markdown("- Can you form any rectangles?")
            st.markdown("- What would be the minimum area?")
            
            predicted_area = st.number_input("What area do you expect?", 
                                           min_value=0, value=0, step=1)
            
            if st.button("Check My Prediction!", type="primary"):
                actual_area, steps = min_area_rect(points)
                st.session_state.attempts += 1
                
                if predicted_area == actual_area:
                    st.session_state.score += 1
                    st.markdown(f"""
                    <div class="success-box">
                        🎉 <strong>Correct!</strong> The minimum area is indeed {actual_area}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="warning-box">
                        🔍 <strong>Not quite!</strong> You predicted {predicted_area}, but the actual minimum area is {actual_area}
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Understanding Questions")
            
            with st.expander("💭 Why do we use a Set?"):
                answer1 = st.text_input("Your answer:", key="q1")
                if st.button("Check Answer 1"):
                    if "O(1)" in answer1 or "constant" in answer1.lower() or "fast" in answer1.lower():
                        st.success("✅ Correct! Set provides O(1) lookup time")
                    else:
                        st.info("💡 Hint: Think about time complexity for checking if a point exists")
                        st.write("**Answer:** To check point existence in O(1) time instead of O(n)")
            
            with st.expander("💭 What does the yCord map do?"):
                answer2 = st.text_input("Your answer:", key="q2")
                if st.button("Check Answer 2"):
                    if "group" in answer2.lower() or "same y" in answer2.lower():
                        st.success("✅ Correct! It groups points by y-coordinate")
                    else:
                        st.info("💡 Hint: Think about what points can form horizontal lines")
                        st.write("**Answer:** Groups points by y-coordinate to find potential horizontal sides")
            
            with st.expander("💭 Why check pairs with same y-coordinate?"):
                answer3 = st.text_input("Your answer:", key="q3")
                if st.button("Check Answer 3"):
                    if "horizontal" in answer3.lower() or "same y" in answer3.lower():
                        st.success("✅ Correct! Same y-coordinate means horizontal line")
                    else:
                        st.info("💡 Hint: What kind of line do points with same y-coordinate form?")
                        st.write("**Answer:** Points with same y-coordinate form horizontal sides of rectangles")

with tab3:
    st.markdown("## 🔍 Algorithm Deep Dive")
    
    if 'points' not in st.session_state:
        st.warning("Please set up points in the Problem Setup tab first!")
    else:
        points = st.session_state.points
        
        # Create step-by-step breakdown
        st.markdown("### Step-by-Step Algorithm Execution")
        
        # Step 1: Point Set Creation
        st.markdown("#### Step 1: Create Point Set")
        point_set = set(f"{p[0]},{p[1]}" for p in points)
        st.code(f"pointSet = {point_set}", language='javascript')
        st.markdown("*This allows O(1) lookup to check if a point exists*")
        
        # Step 2: Y-coordinate grouping
        st.markdown("#### Step 2: Group Points by Y-coordinate")
        y_cord = defaultdict(list)
        for point in points:
            y_cord[point[1]].append(point[0])
        
        st.code(f"yCord = {dict(y_cord)}", language='javascript')
        st.markdown("*Groups points that can form horizontal lines*")
        
        # Step 3: Algorithm execution with slider
        st.markdown("#### Step 3: Rectangle Detection Process")
        
        execution_steps = []
        min_area = float('inf')
        
        for y, x_list in y_cord.items():
            if len(x_list) < 2:
                continue
            
            for i in range(len(x_list)):
                for j in range(i + 1, len(x_list)):
                    x1, x2 = x_list[i], x_list[j]
                    
                    for y2, x_list2 in y_cord.items():
                        if y2 == y or len(x_list2) < 2:
                            continue
                        
                        if f"{x1},{y2}" in point_set and f"{x2},{y2}" in point_set:
                            area = abs(x2 - x1) * abs(y2 - y)
                            execution_steps.append({
                                'step': len(execution_steps) + 1,
                                'horizontal_line_1': f"y = {y}, x values: [{x1}, {x2}]",
                                'horizontal_line_2': f"y = {y2}, x values: found {x1} and {x2}",
                                'rectangle': f"({x1},{y}), ({x2},{y}), ({x1},{y2}), ({x2},{y2})",
                                'area': area,
                                'width': abs(x2 - x1),
                                'height': abs(y2 - y)
                            })
                            min_area = min(min_area, area)
        
        if execution_steps:
            step_num = st.slider("Navigate through steps:", 0, len(execution_steps) - 1, 0)
            
            current_step = execution_steps[step_num]
            st.markdown(f"**Step {current_step['step']}:**")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"**Horizontal Line 1:** {current_step['horizontal_line_1']}")
                st.markdown(f"**Horizontal Line 2:** {current_step['horizontal_line_2']}")
                st.markdown(f"**Rectangle Found:** {current_step['rectangle']}")
            
            with col2:
                st.metric("Width", current_step['width'])
                st.metric("Height", current_step['height'])
                st.metric("Area", current_step['area'])
            
            if current_step['area'] == min_area:
                st.success("🎯 This is the minimum area rectangle!")
        else:
            st.info("No rectangles can be formed with these points.")
        
        # Final result
        final_result = 0 if min_area == float('inf') else min_area
        st.markdown(f"### Final Result: **{final_result}**")

with tab4:
    st.markdown("## 📊 Visual Analysis")
    
    if 'points' not in st.session_state:
        st.warning("Please set up points in the Problem Setup tab first!")
    else:
        points = st.session_state.points
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Main visualization
            fig, ax = plt.subplots(figsize=(10, 8))
            
            if points:
                x_coords = [p[0] for p in points]
                y_coords = [p[1] for p in points]
                
                # Plot points
                ax.scatter(x_coords, y_coords, c='red', s=150, alpha=0.7, zorder=5)
                
                # Annotate points
                for i, (x, y) in enumerate(points):
                    ax.annotate(f'({x},{y})', (x, y), xytext=(5, 5), 
                              textcoords='offset points', fontsize=10, fontweight='bold')
                
                # Find and draw rectangles
                min_area, steps = min_area_rect(points)
                
                if steps:
                    # Draw all possible rectangles
                    colors = plt.cm.Set3(np.linspace(0, 1, len(steps)))
                    
                    for i, step in enumerate(steps):
                        rect_points = step['rectangle']
                        # Sort points to draw rectangle properly
                        x_vals = [p[0] for p in rect_points]
                        y_vals = [p[1] for p in rect_points]
                        
                        # Draw rectangle
                        x_min, x_max = min(x_vals), max(x_vals)
                        y_min, y_max = min(y_vals), max(y_vals)
                        
                        rect = plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                                           linewidth=2, edgecolor=colors[i], 
                                           facecolor=colors[i], alpha=0.3)
                        ax.add_patch(rect)
                        
                        # Label the rectangle
                        ax.text(x_min + (x_max - x_min) / 2, y_min + (y_max - y_min) / 2,
                               f'Area: {step["area"]}', ha='center', va='center',
                               fontsize=9, fontweight='bold',
                               bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
                
                ax.grid(True, alpha=0.3)
                ax.set_xlabel('X Coordinate', fontsize=12)
                ax.set_ylabel('Y Coordinate', fontsize=12)
                ax.set_title('Points and Rectangles Visualization', fontsize=14, fontweight='bold')
                
                # Set axis limits with some padding
                if x_coords and y_coords:
                    x_margin = (max(x_coords) - min(x_coords)) * 0.1 + 1
                    y_margin = (max(y_coords) - min(y_coords)) * 0.1 + 1
                    ax.set_xlim(min(x_coords) - x_margin, max(x_coords) + x_margin)
                    ax.set_ylim(min(y_coords) - y_margin, max(y_coords) + y_margin)
            
            st.pyplot(fig)
        
        with col2:
            st.markdown("### Analysis Summary")
            
            min_area, steps = min_area_rect(points)
            
            st.metric("Total Points", len(points))
            st.metric("Rectangles Found", len(steps))
            st.metric("Minimum Area", min_area)
            
            if steps:
                st.markdown("### Rectangle Details")
                df = pd.DataFrame([
                    {
                        'Rectangle': i + 1,
                        'Width': step['width'],
                        'Height': step['height'],
                        'Area': step['area'],
                        'Is Minimum': step['area'] == min_area
                    }
                    for i, step in enumerate(steps)
                ])
                st.dataframe(df)
            
            st.markdown("### Data Structures State")
            
            # Show point set
            point_set = set(f"{p[0]},{p[1]}" for p in points)
            st.markdown("**Point Set:**")
            st.code(str(point_set))
            
            # Show y-coordinate grouping
            y_cord = defaultdict(list)
            for point in points:
                y_cord[point[1]].append(point[0])
            
            st.markdown("**Y-Coordinate Grouping:**")
            st.code(str(dict(y_cord)))

with tab5:
    st.markdown("## 🧪 Debug Mode")
    
    if 'points' not in st.session_state:
        st.warning("Please set up points in the Problem Setup tab first!")
    else:
        points = st.session_state.points
        
        debug_mode = st.checkbox("Enable Debug Mode")
        
        if debug_mode:
            st.markdown("### Detailed Algorithm Trace")
            
            # Show each step in detail
            point_set = set(f"{p[0]},{p[1]}" for p in points)
            y_cord = defaultdict(list)
            for point in points:
                y_cord[point[1]].append(point[0])
            
            st.markdown("#### Initial Data Structures")
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("**Point Set:**")
                for point in point_set:
                    st.code(f"'{point}' in pointSet")
            
            with col2:
                st.markdown("**Y-Coordinate Map:**")
                for y, x_list in y_cord.items():
                    st.code(f"y={y}: x_values={x_list}")
            
            st.markdown("#### Algorithm Execution Trace")
            
            min_area = float('inf')
            step_count = 0
            
            for y, x_list in y_cord.items():
                if len(x_list) < 2:
                    st.info(f"Skipping y={y} (only {len(x_list)} point(s))")
                    continue
                
                st.markdown(f"**Processing y={y} with x_values={x_list}**")
                
                for i in range(len(x_list)):
                    for j in range(i + 1, len(x_list)):
                        x1, x2 = x_list[i], x_list[j]
                        step_count += 1
                        
                        st.markdown(f"*Step {step_count}: Checking horizontal line at y={y} from x={x1} to x={x2}*")
                        
                        found_rectangle = False
                        for y2, x_list2 in y_cord.items():
                            if y2 == y or len(x_list2) < 2:
                                continue
                            
                            point1_exists = f"{x1},{y2}" in point_set
                            point2_exists = f"{x2},{y2}" in point_set
                            
                            if point1_exists and point2_exists:
                                area = abs(x2 - x1) * abs(y2 - y)
                                min_area = min(min_area, area)
                                found_rectangle = True
                                
                                st.success(f"✅ Rectangle found! Points: ({x1},{y}), ({x2},{y}), ({x1},{y2}), ({x2},{y2})")
                                st.write(f"   Width: {abs(x2 - x1)}, Height: {abs(y2 - y)}, Area: {area}")
                                
                                if area == min_area:
                                    st.write("   🎯 This is the current minimum!")
                        
                        if not found_rectangle:
                            st.write("   ❌ No matching horizontal line found")
            
            final_result = 0 if min_area == float('inf') else min_area
            st.markdown(f"### Final Result: **{final_result}**")
            
            # Performance analysis
            st.markdown("### Performance Analysis")
            n = len(points)
            st.write(f"- Input size: {n} points")
            st.write(f"- Point set creation: O({n})")
            st.write(f"- Y-coordinate grouping: O({n})")
            st.write(f"- Rectangle checking: O({n}²) in worst case")
            st.write(f"- Total time complexity: O({n}²)")
            st.write(f"- Space complexity: O({n})")

# Footer
st.markdown("---")
st.markdown("### 🎯 Learning Tips")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Algorithm Strategy:**
    - Fix one horizontal side
    - Find matching horizontal side
    - Check if vertical sides exist
    - Track minimum area
    """)

with col2:
    st.markdown("""
    **Key Insights:**
    - Set enables O(1) point lookup
    - Map groups potential horizontal sides
    - Rectangle needs 4 specific points
    - Brute force is acceptable for small inputs
    """)

with col3:
    st.markdown("""
    **Common Mistakes:**
    - Forgetting to check all 4 corners
    - Not handling edge cases (< 4 points)
    - Inefficient point existence checking
    - Missing minimum area tracking
    """)

st.markdown("---")
st.markdown("*💡 Keep practicing with different test cases to master the algorithm!*")