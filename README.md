# HSC Physics 复习手册（Module 5–8）

给 NSW HSC Physics 考生用的**免费英文复习资料**，覆盖 Year 12 的四个 Module。
写给基础比较弱、英语不是母语的同学：句子短，每个专业词第一次出现都有解释，推导和计算每一步都写出来。

> **English summary.** Free, plain-English revision guides for NSW HSC Physics, Year 12
> (Modules 5–8, Physics Stage 6 Syllabus 2017), with worked examples, practice questions and full
> worked answers. Download the PDFs from [Releases](https://github.com/OrientalDaitou/hsc-physics-revision/releases/latest).
> This is an independent, unofficial project. It is not affiliated with or endorsed by NESA or any school.

## 适用范围

- **考纲：** Physics Stage 6 Syllabus (2017) 的 Year 12 部分（Module 5–8）。
- **适用考试：** 用这份考纲的 HSC 考试（包括 2026 年 HSC）。新的 Physics 11–12 Syllabus (2025) 从 2028 年才开始考，内容有变化，这套资料不覆盖新考纲。

## 有哪些资料

直接下载 PDF：**[Releases 页面](https://github.com/OrientalDaitou/hsc-physics-revision/releases/latest)**（不用装任何软件）。

| 资料 | 说明 |
|---|---|
| **Revision 完整版**（每个 Module 一本，约 210–230 页） | 从零讲起：概念 → 公式卡 → 例题 → 常见错误 → HSC 答题技巧 → 小测。书末有公式表讲解、术语表（附中文）、练习题和完整解答、考前一页总结 |
| **Essentials 精简版**（每本约 45–50 页） | 完整版的浓缩，适合已经学过、想快速过一遍的同学 |
| **选择题册 + 答案**（MC Booklet） | 每个 Module 70 道左右新编选择题，按主题排，答案有完整解题过程 |
| **简答题册 + 评分标准**（Short Answer） | HSC Section II 风格的简答题，答案附评分要点和示范答案 |
| **M5 引力专题**（M5T3 Gravity） | Module 5 万有引力部分的 30 道选择题（小测版和带讲解的题册版） |
| **真题题号索引**（MCQ Index，Module 6–8） | 列出 2019–2025 年 HSC 选择题中考哪个 Module、考什么知识点和答案字母。**不含原题**，原题请到 NESA 官网下载 |

### 怎么用

1. 先看 **Revision 完整版**，每节学完做 Quick check。
2. 一章学完后，做对应的**选择题册**和**简答题册**，对照答案找漏洞。
3. 考前看 **Essentials 精简版**和书末的 **Last-minute summary**。
4. 用**真题题号索引**找到对应年份的 HSC 真题，到 [NESA 官网](https://www.nsw.gov.au/education-and-training/nesa/curriculum/hsc-exam-papers) 下载原卷来练。

## 从源码重新生成 PDF

PDF 是用 LaTeX（一种排版软件）从 `src/` 里的源码编译出来的。想修改内容或自己生成，需要：

1. 安装 TeX Live 2024 或更新版本（macOS 上装 [MacTeX](https://www.tug.org/mactex/)），里面已经带了 XeLaTeX 和 latexmk。
2. 在仓库根目录运行：

   ```bash
   ./build.sh            # 生成全部 PDF（大约 10–20 分钟）
   ./build.sh mod6       # 只生成某一本，名字就是 src/ 里的文件夹名
   ```

   生成的 PDF 放在 `pdf/` 文件夹。

3. （可选）书里的数据图是用 Python 画的，图已经生成好放在各 `figures/` 文件夹里。改了数据想重画，需要 Python 3、numpy 和 matplotlib：

   ```bash
   python3 src/mod7/figures/ch1_blackbody.py
   ```

4. （可选）`checks/` 里是每本题册的数值核对脚本，用来重算题目里的每一个数字：

   ```bash
   python3 checks/m6-mc-booklet/numbers.py
   ```

### 文件夹说明

```
src/
  common/            四本书共用的排版模板（hscphys.sty）和画图工具
  mod5 … mod8/       Revision 完整版（main.tex 是入口）
  mod5_essentials …  Essentials 精简版
  m5_mc_booklet …    选择题册（booklet.tex 题目，answers.tex 答案）
  m5_short_answer …  简答题册（questions.tex 题目，answers.tex 评分标准）
  m5t3_booklet, m5t3_quiz   M5 引力专题
  m6_hsc_index …     真题题号索引
checks/              题册的数值核对脚本
build.sh             一键编译
```

## 声明

- 这是**个人、非官方**的学习资料，与 **NESA（NSW Education Standards Authority）和任何学校都没有关系**，也没有得到它们的认可。HSC 是 NESA 的考试名称。
- 资料里的讲解、例题和练习题都是作者自己写的，**没有收录 NESA 真题或评分标准的原文**。真题索引只写了年份、题号、作者自己概括的知识点和答案字母。
- 公式写法参照 NESA 官方公式表，请以考试时发的官方 Formulae and Data Sheet 为准。
- 作者尽力核对过每一道题，但难免有错。发现错误欢迎在 [Issues](https://github.com/OrientalDaitou/hsc-physics-revision/issues) 里指出。

## 授权

- **文字内容和 PDF**：[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans)（见 [LICENSE](LICENSE)）。可以免费使用、打印、分享和修改，但要**注明出处**、**不能用于商业用途**，修改后的版本也要用同样的授权。
- **代码**（`build.sh`、`.py` 脚本、`.sty` 排版模板）：[MIT](LICENSE-CODE)。
