#!/usr/bin/env bash
# build.sh -- compile the PDFs from the LaTeX sources in src/.
#
#   ./build.sh            build everything (about 10-20 minutes)
#   ./build.sh mod5       build one folder of src/ (e.g. mod6_essentials, m7_mc_booklet)
#
# Needs XeLaTeX and latexmk (TeX Live 2024 or newer). Finished PDFs go to pdf/.
# Build files (aux, log, ...) go to build/.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH="/Library/TeX/texbin:$PATH"

# folder:file.tex:output-name (without .pdf)
TARGETS=(
  mod5:main.tex:Module5_Advanced_Mechanics_Revision
  mod6:main.tex:Module6_Electromagnetism_Revision
  mod7:main.tex:Module7_Nature_of_Light_Revision
  mod8:main.tex:Module8_Universe_to_Atom_Revision
  mod5_essentials:main.tex:Module5_Advanced_Mechanics_Essentials
  mod6_essentials:main.tex:Module6_Electromagnetism_Essentials
  mod7_essentials:main.tex:Module7_Nature_of_Light_Essentials
  mod8_essentials:main.tex:Module8_Universe_to_Atom_Essentials
  m5_mc_booklet:booklet.tex:M5_MC_Booklet
  m5_mc_booklet:answers.tex:M5_MC_Booklet_Answers
  m5_short_answer:questions.tex:M5_Short_Answer
  m5_short_answer:answers.tex:M5_Short_Answer_Marking
  m5_short_answer_2:questions.tex:M5_Short_Answer_Set2
  m5_short_answer_2:answers.tex:M5_Short_Answer_Set2_Marking
  m5t3_booklet:main.tex:M5T3_Gravity_MC_Booklet
  m5t3_quiz:quiz.tex:M5T3_Gravity_MC_Quiz
  m5t3_quiz:quiz_answers.tex:M5T3_Gravity_MC_Quiz_Answers
  m6_mc_booklet:booklet.tex:M6_MC_Booklet
  m6_mc_booklet:answers.tex:M6_MC_Booklet_Answers
  m6_short_answer:questions.tex:M6_Short_Answer
  m6_short_answer:answers.tex:M6_Short_Answer_Marking
  m6_hsc_index:index.tex:HSC_Module6_MCQ_Index_2019-2025
  m7_mc_booklet:booklet.tex:M7_MC_Booklet
  m7_mc_booklet:answers.tex:M7_MC_Booklet_Answers
  m7_short_answer:questions.tex:M7_Short_Answer
  m7_short_answer:answers.tex:M7_Short_Answer_Marking
  m7_hsc_index:index.tex:HSC_Module7_MCQ_Index_2019-2025
  m8_mc_booklet:booklet.tex:M8_MC_Booklet
  m8_mc_booklet:answers.tex:M8_MC_Booklet_Answers
  m8_short_answer:questions.tex:M8_Short_Answer
  m8_short_answer:answers.tex:M8_Short_Answer_Marking
  m8_hsc_index:index.tex:HSC_Module8_MCQ_Index_2019-2025
)

mkdir -p "$ROOT/pdf" "$ROOT/build"
failed=()
for t in "${TARGETS[@]}"; do
  IFS=: read -r dir tex name <<<"$t"
  if [ $# -gt 0 ] && [ "$1" != "$dir" ]; then continue; fi
  echo "==> src/$dir/$tex  ->  pdf/$name.pdf"
  out="$ROOT/build/$dir/${tex%.tex}"
  mkdir -p "$out"
  # books find hscphys.sty in ../common; the quiz booklets use their own quiz.sty
  if (cd "$ROOT/src/$dir" && TEXINPUTS=".:$ROOT/src/common//:" \
        latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir="$out" "$tex" >"$out/build.txt" 2>&1); then
    cp "$out/${tex%.tex}.pdf" "$ROOT/pdf/$name.pdf"
  else
    echo "    FAILED -- see $out/build.txt"
    failed+=("$dir/$tex")
  fi
done

if [ ${#failed[@]} -gt 0 ]; then
  echo "Failed: ${failed[*]}"
  exit 1
fi
echo "Done. PDFs are in pdf/"
