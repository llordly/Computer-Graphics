# <center>Class Assignment 3 Report</center>

 

**2017029589 류지범**

 

# #0

- 모든 요구사항과 extra credit을 다 구현했으며, 아래는 해당 요구사항에 대한 구현 내용이다.



## #1 

- 우선 ClassAssignment1의 카메라와 grid plane을 사용했다.
- Drop-call-back을 사용해서 bvh파일을 window에 drop하면 skeleton이 나오도록 했다.
  - 처음엔 skeleton이 t-pose로 나온다.
  - Hierarchical하게 line으로 joint들이 이어지도록 했고 end site까지도 이어질 수 있도록 했다.

- `E` 키를 누르면 line으로 잇는 것이 아닌 obj 파일로 잇도록 했다.(extra credit)
  - Obj파일로 그리는 경우 ClassAssignment와 동일하게 lighting, shading이 다 구현되어 있고, s를 누르면 smooth shading, z를 누르면 wireframe 모드가 바뀌도록 구현되어 있다.

- `spacebar`를 누르면 motion을 동작하도록 했다. Glfw.swap_interval(1)로 고정했고, 파일의 fps에 따라 속도를 조절하게 했으며, fps가 60을 넘어갈 경우 그냥 60fps로 고정했다.

- Bvh파일을 drop하면 file name, number of frames, FPS, Number of joints, List of all joint names가 나오도록 했다.
  - <img src=''>

- 복싱을 하는 모션 파일을 다운받아서 사용했으며 해당 애니메이션 링크는 다음과 같다.
  - https://youtu.be/7zP5zMgpqeY

- 다음은 sample 파일을 그린 것이고 왼쪽은 line skeleton, 오른쪽은 obj로 그린 것이다.

viii. 

|      |      |
| ---- | ---- |


 다음은 sample 파일의 motion이다.

ix.  

|      |                                                              |      |                                                              |      |                                                              |
| ---- | ------------------------------------------------------------ | ---- | ------------------------------------------------------------ | ---- | ------------------------------------------------------------ |
|      | ![알 수 없음_2.png](blob:file:///7ed61b63-aaf3-451c-b4c2-022a1c999647) |      | ![알 수 없음_3.png](blob:file:///c060ea6e-9d03-4dd8-8e62-de83af9fd3e9) |      | ![알 수 없음_4.png](blob:file:///5d3bac7c-c19f-4a8a-9d75-c7e4fd6cf7d5) |
|      |                                                              |      |                                                              |      |                                                              |


 다음은 download bvh의 skeleton과 motion이다.
