//////////////////////////////////////////////////////////////////////////////////////
// Лабораторная работа 5 по дисциплине ЛОИС
// Выполнена студентами группы 921702 БГУИР
// Тарамин Д.В. и Валюкевич В.И.
// Вариант 8. Реализовать обратный нечеткий логический вывод на основе операции нечеткой композиции (max({max({0} ∪ {x_i + y_i - 1}) | i}))
// 13.09.2022
// Использованные материалы:
// Логические основы интеллектуальных систем. Практикум : учеб.-метод. пособие / В.В. Голенков [и др.] Минск : БГУИР, 2011. – 70 с.

#include <algorithm>
#include <cstddef>
#include <fstream>
#include <iostream>
#include <iterator>
#include <map>
#include <memory>
#include <string>
#include <type_traits>
#include <vector>

#include "fuzzy_set_types.h"

Solutions calculateSolution(const FuzzySet &ySet, const RelationMatrix &rel);

bool addRange(Solutions &sols, size_t varNum, const Range &newRange);

bool addSolutions(Solutions &sols, const std::map<size_t, Range> &newRanges);

Solutions uniteSolutions(const Solutions &sols);

void read(std::ifstream &input, std::vector<FuzzySet> &sets, std::vector<Relation> &rels,
          std::vector<ReverseConclusion> &concls);

template <typename T>
std::vector<T> readSets(std::ifstream &input);

std::vector<Relation> readRelations(std::ifstream &input);

template <typename T>
void validateNames(const std::vector<T> &vect);

template <typename T>
const T &findByName(const std::vector<T> &vect, const Name &name);

int main() {
  std::ifstream input(INPUT_FILE_PATH);
  std::ofstream output(OUTPUT_FILE_PATH);

  try {
    std::vector<FuzzySet> sets;
    std::vector<Relation> rels;
    std::vector<ReverseConclusion> concls;
    read(input, sets, rels, concls);

    for (auto &concl : concls) {
      const Relation &rel = findByName(rels, concl.getRelationName());
      const FuzzySet &ySet = findByName(sets, concl.getYSetName());

      if (rel.getMatrix().front().size() != ySet.size()) {
        throw std::invalid_argument("");
      }

      concl.setSolutions(calculateSolution(ySet, rel.getMatrix()));

      output << concl.toString() << "\n";
    }
  } catch (...) {
    output << "Invalid input\n";
  }
}

Solutions calculateSolution(const FuzzySet &ySet, const RelationMatrix &rel) {
  Solutions sols = {Solution(rel.size(), {0.0, 1.0})};

  for (size_t i = 0; i < rel.front().size(); i++) {
    std::map<size_t, Range> newRanges;
    double ySetVal = ySet[i].getVal();

    for (size_t j = 0; j < rel.size(); j++) {
      double xSetVal = ySetVal - rel[j][i] + 1;

      if (xSetVal <= 1.0) {
        if (!addRange(sols, j, {0, xSetVal})) {
          return {};
        }

        newRanges.insert({j, {xSetVal, xSetVal}});
      }
    }

    if (ySetVal == 0) {
      continue;
    }

    if (!addSolutions(sols, newRanges)) {
      return {};
    }
  }

  return sols;
}

bool addRange(Solutions &sols, size_t varNum, const Range &newRange) {
  for (auto &sol : sols) {
    Range &range = sol[varNum];

    if (newRange.first > range.first) {
      range.first = newRange.first;
    }
    if (newRange.second < range.second) {
      range.second = newRange.second;
    }

    if (range.first > range.second) {
      return false;
    }
  }

  return true;
}

bool addSolutions(Solutions &sols, const std::map<size_t, Range> &newRanges) {
  if (newRanges.empty()) {
    return false;
  }

  Solutions newSols;

  for (const auto &p : newRanges) {
    size_t varNum = p.first;
    const Range &newRange = p.second;

    size_t oldSize = newSols.size();

    for (const auto &sol : sols) {
      if (const Range &range = sol[varNum]; newRange.first < range.first || newRange.second > range.second) {
        continue;
      }

      newSols.emplace_back(sol);
      newSols.back()[varNum] = newRange;
    }

    if (newSols.size() == oldSize) {
      return false;
    }
  }

  sols = uniteSolutions(newSols);

  return true;
}

Solutions uniteSolutions(const Solutions &sols) {
  Solutions uniteSols = {sols.front()};

  for (size_t i = 1; i < sols.size(); i++) {
    const Solution &solToAdd = sols[i];
    bool shouldAdd = true;

    for (const auto &sol : uniteSols) {
      bool isSubRange = true;

      for (size_t i = 0; i < solToAdd.size(); i++) {
        if (solToAdd[i].first < sol[i].first || solToAdd[i].second > sol[i].second) {
          isSubRange = false;
          break;
        }
      }

      if (isSubRange) {
        shouldAdd = false;
        break;
      }
    }

    if (shouldAdd) {
      uniteSols.emplace_back(solToAdd);
    }
  }

  return uniteSols;
}

void read(std::ifstream &input, std::vector<FuzzySet> &sets, std::vector<Relation> &rels,
          std::vector<ReverseConclusion> &concls) {
  sets = readSets<FuzzySet>(input);
  validateNames(sets);

  rels = readRelations(input);
  validateNames(rels);

  concls = readSets<ReverseConclusion>(input);
}

template <typename T>
std::vector<T> readSets(std::ifstream &input) {
  std::vector<T> vect;
  std::string str;

  while (std::getline(input, str)) {
    if (str.empty()) {
      break;
    }
    vect.emplace_back(str);
  }

  return vect;
}

std::vector<Relation> readRelations(std::ifstream &input) {
  std::vector<Relation> vect;
  std::string inStr;
  std::string relStr;

  while (std::getline(input, inStr)) {
    if (inStr.empty()) {
      break;
    }

    relStr += inStr;

    if (relStr.back() == ')') {
      vect.emplace_back(relStr);
      relStr.clear();
    } else {
      relStr += "\n";
    }
  }

  return vect;
}

template <typename T>
void validateNames(const std::vector<T> &vect) {
  for (size_t i = 0; i < vect.size() - 1; i++) {
    const Name &name = vect[i].getName();
    auto setIter = std::find_if(vect.begin() + i + 1, vect.end(), [name](const T &el) { return el.getName() == name; });

    if (setIter != vect.end()) {
      throw std::invalid_argument("");
    }
  }
}

template <typename T>
const T &findByName(const std::vector<T> &vect, const Name &name) {
  auto setIter = std::find_if(vect.begin(), vect.end(), [name](const T &el) { return el.getName() == name; });

  if (setIter == vect.end()) {
    throw std::invalid_argument("");
  }

  return *setIter;
}
