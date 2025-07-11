## Build and Setup Instructions  
1. **Put this into any ROS 2 workspace** (Example: `~/ros2_ws/src`)  
   ```bash
   cd ~/ros2_ws/src
   # Copy your package folder here
   ```  
2. **Build the workspace**  
   ```bash
   cd ~/ros2_ws
   colcon build
   ```  
3. **Source the workspace**  
   ```bash
   cd week4_arm
   source install/setup.bash
   ```  
4. **Make launch scripts executable**  
   ```bash
   cd launch
   chmod +x *.py
   ```

## ️RViz2 Setup Instructions  
1. **Launch the robot model in RViz2**  
   ```bash
   ros2 launch week4_arm display_arm.launch.py
   ```  
2. **In RViz2:**  
   - Click on **Global Options** in the left panel.  
   - Set **Fixed Frame** to `base_link`.  
3. **Add the Robot Model:**  
   - Click **Add** at the bottom left panel.  
   - Choose **RobotModel**.  
   - In the **Description Topic**, set it to `robot_description`.  
   ✅ You should now see the 2‑D robot‑arm model in the display window.  
4. *(Optional)* **Add TF to visualise frames:**  
   - Click **Add**.  
   - Choose **TF** to visualise the coordinate frames of your robot.  
   - Red = X‑axis, Green = Y‑axis, Blue = Z‑axis.  

---

# Week‑4 Robotic‑Arm Assignment (ELEC)

> A ROS 2 implementation of a 2‑link planar arm covering **Forward Kinematics (Q1)**, an **Inverse‑Kinematics reachability study (Q2)** and an **interactive IK goal node (Q3)**.

| Folder / File | Purpose |
|---------------|---------|
| `week4_arm/` | Complete ROS 2 package (URDF, launch, nodes) |
| `demo.mp4` | Screen‑capture showing real‑time FK updates in RViz2 |
| `week4_q2.jpg` | Hand‑written derivation for Q2 |
| `week4_q2_final_answers.xlsx` | Spreadsheet with numeric IK solutions |
| `README.md` | *This* guide |

---

## 1  Q1 – Forward Kinematics Node

*Node:* `week4_arm/scripts/fk_node`
*Topic flow:*

```
/joint_states     → FK node → /end_effector_position
                (θ₁,θ₂)        (x,y)
```

- Adds **π/2** offset to the shoulder joint per the PDF.  
- Publishes `geometry_msgs/msg/Point` with **x & y** only.  
- Tested in RViz2; see *demo.mp4* in this repo.

### Quick run

```bash
ros2 run week4_arm fk_node
```

---

## 2  Q2 – Reachability & IK Solutions

| # | Target (x,y) [m] | Reachable? | θ₁ [rad] | θ₂ [rad] |
|---|------------------|------------|----------|----------|
| 1 | (2.0, 1.0) | ✅ | see Excel | see Excel |
| 2 | (3.0, 0.0) | ✅ |           |           |
| 3 | (0.0, 3.4) | ✅ |           |           |
| 4 | (0.0, ‑2.5) | ✅ |           |           |
| 5 | (4.0, 0.0) | ❌ – outside max reach (≥3.5 m) | – | – |
| 6 | (0.0, 0.2) | ❌ – inside min reach (≤0.5 m) | – | – |

For full derivations see **`week4_q2.jpg`**; numerical values are tabulated in **`week4_q2_final_answers.xlsx`** 

---

## 3  Q3 – Continuation of Q1

*Node:* `week4_arm/scripts/move_effector`

1. Subscribes to `/end_effector_position`  
2. Prompts the user: axis (`x`/`y`) & step (≤ 0.5 m).  
3. Computes IK; verifies workspace limits (0.5 m ≤ ρ ≤ 3.5 m).  
4. Publishes `[θ₁, θ₂]` on `/joint_angles_goal` (`std_msgs/Float64MultiArray`).

```bash
ros2 run week4_arm move_effector
```



---

## Demo Video

<details>
<p align="center">
  <video src="demo.mp4" width="600" controls></video>
</p>

</details>

---


---

## Author

**Aksh (aksh‑0407)** – Week‑4 submission.


