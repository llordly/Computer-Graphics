# <center>Class Assignment 2 Report</center>

 

**2017029589 류지범**

 

## #0

- 모든 요구사항과 extra credit을 다 구현했으며, 아래는 해당 요구사항에 대한 구현 내용이다.



## #1 Manipulate the camera

- ClaassAssignment1의 코드를 기본으로 사용해서 카메라 움직임을 구현했다.



## #2 Single mesh rendering mode

- 프로그램이 처음 실행하면 **single mesh mode**로 실행되도록 했다.
- Obj 파일을 윈도우에 drop하면 obj 파일이 렌더링되도록 했고, 다른 obj 파일을 drop하면 기존의 것은 사라지고 다른 obj 파일이 렌더링되도록 했다.
- Obj 파일에서 v, vn, f 정보만 파싱해서 array에 넣었고 `glDrawArray()`와 `glDrawElements()`를 사용해서 삼각형을 그리도록 했다.
- Obj 파일을 drop하면, file name, total number of faces, number of faces with 3 vertices, number of faces with 4 vertices, number of faces with more than 4 vertices가 콘솔에 출력되도록 했다.



## #3 Animating hierarchical model rendering mode

- `H` 키를 누르면 날아다니는 헬리콥터 모델이 나오도록 렌더링했다.
- 파일들은 소스 파일이 있는 폴더에 함께 넣었고, 상대 경로로 프로그램 시작 시 읽어오도록 했다. Obj 파일은 다운받은 3개의 다른 파일을 사용했다.
- Hierarchical 하게 구현은 OpenGL matrix stack을 사용했다. 4 level로 구현했으며, 헬리콥터 본체-프로펠러, 본체-사다리1, 사다리1-사다리2, 사다리2-사다리3 의 구조로 이루어져있다.
- 헬리콥터는 원 궤적으로 돌고, 프로펠러는 헬리콥터 본체에 붙어 회전하고, 사다리1은 헬리콥터에 붙어서 20도 정도로 앞뒤로 움직이고, 사다리2는 사다리1에 붙어 상대적으로 20도 정도로 앞뒤로 움직이고, 사다리3은 사다리2에 붙어 상대적으로 20도 정도로 앞뒤로 움직인다.



## #4 Lighting & Etc

- Light source는 3가지를 사용했다.

- 1번 light는 (-50., 50., -50), 2번 light는 (50., 50., 50.), 3번 light는 (-20., 20., 20.)에 위치해있으며, 2번만 directional light이고 1, 3번은 point light이다.
- 1번 light는 청록(0/255, 130/255, 153/255), 2번 light는 보라(128/255, 65/255, 217/255), 3번 light는 진한빨강(152/255, 0/255, 0/255)를 사용했다.
- Hierarchical mode, single mode 모두 Object의 color는 흰색으로 했다.
- 1번 light는 `GL_LIGHT0`, 2번 light는 `GL_LIGHT2`, 3번 light는 `GL_LIGHT7`를 사용했다.
- `Z` 키를 누르면 solid 모드로 실행되도록 했다. 프로그램 실행 시 기본은 wireframe 모드이고, `Z`키를 누르면 `GL_FIL`L을 사용해서 도형의 프레임이 채워지도록 했다.



## #5 Extra credits

- `S`키를 누르면 **forced smooth shading mode**가 되도록 했다. 특정 vertex의 normal vector들을 다 더한 vector에서 더한 벡터의 크기를 나눈 것을 그 vertex의 normal vector로 지정하도록 했다.
- 삼각형이 아닌 n-polygon들로 구성된 face들도 다 렌더링되도록 구현했다. Obj 파일에서 face 정보를 읽을 때, triangulation algorithm을 사용해서, face가 4개 이상의 vertex로 이루어져 있을 경우, 3개짜리로 다 쪼갠 후에 index array와 vertex array에 넣도록 했고, `glDrawArrays()`, `glDrawElements()`를 사용해서 렌더링하도록 했다.
- Hierarchical model의 youtube link는 다음과 같다.
  - https://youtu.be/jpR97puEKvA
