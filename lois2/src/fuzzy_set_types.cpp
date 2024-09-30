//////////////////////////////////////////////////////////////////////////////////////
// Лабораторная работа 5 по дисциплине ЛОИС
// Выполнена студентами группы 921702 БГУИР
// Тарамин Д.В. и Валюкевич В.И.
// Вариант 8. Реализовать обратный нечеткий логический вывод на основе операции нечеткой композиции (max({max({0} ∪ {x_i + y_i - 1}) | i}))
// 13.09.2022
// Использованные материалы:
// Логические основы интеллектуальных систем. Практикум : учеб.-метод. пособие / В.В. Голенков [и др.] Минск : БГУИР, 2011. – 70 с.

#include "fuzzy_set_types.h"
#include <cstdlib>
#include <sstream>
#include <string>
#include <utility>

Name::Name(const std::string &str) : ch(str.front()) {
  const std::string numStr = str.substr(1);
  if (!numStr.empty()) {
    num = int32_t(std::stoul(numStr));
  }
}

std::string Name::toString() const {
  if (num != -1) {
    return ch + std::to_string(num);
  }
  if (ch == -1) {
    return "";
  }
  return std::string(1, ch);
}

bool Name::operator==(const Name &rhs) const {
  return ch == rhs.ch && num == rhs.num;
}

bool Name::operator!=(const Name &rhs) const {
  return !(*this == rhs);
}

bool Name::operator<(const Name &rhs) const {
  if (ch != rhs.ch) {
    return ch < rhs.ch;
  }
  return num < rhs.num;
}

SetName::SetName(const std::string &str) : Name(str) {
  if (str.front() < 'A' || str.front() > 'Z') {
    throw std::invalid_argument("");
  }
}

RelationName::RelationName(const std::string &str) : Name(str) {
  if (str.front() < 'a' || str.front() > 'z') {
    throw std::invalid_argument("");
  }
}

SetElemName::SetElemName(const std::string &str) : Name(str) {
  if (str.front() < 'a' || str.front() > 'z') {
    throw std::invalid_argument("");
  }
}

FuzzySetElem::FuzzySetElem(const SetElemName &inVar, double inVal) : var(inVar), val(inVal) {
}

FuzzySetElem::FuzzySetElem(std::string str) {
  if (str.front() != '(' || str.back() != ')') {
    throw std::invalid_argument("");
  }

  str = str.substr(1);
  str.pop_back();

  {
    const size_t i = str.find(',');
    if (i == std::string::npos) {
      throw std::invalid_argument("");
    }

    var = SetElemName(str.substr(0, i));
    val = std::stod(str.substr(i + 1));
  }

  if (val < 0 || val > 1) {
    throw std::invalid_argument("");
  }
}

SetElemName FuzzySetElem::getVar() const {
  return var;
}

double FuzzySetElem::getVal() const {
  return val;
}

std::string FuzzySetElem::toString() const {
  return "(" + var.toString() + "," + std::to_string(val) + ")";
}

bool FuzzySetElem::operator<(const FuzzySetElem &el) const {
  return var < el.var;
}

FuzzySet::FuzzySet(std::string str) {
  const size_t i = str.find('=');
  if (i == std::string::npos) {
    throw std::invalid_argument("");
  }

  name = SetName(str.substr(0, i));
  str = str.substr(i + 1);

  if (str.front() != '{' || str.back() != '}') {
    throw std::invalid_argument("");
  }

  str = str.substr(1);
  str.pop_back();

  for (;;) {
    size_t i = str.find(')');
    if (i == std::string::npos) {
      throw std::invalid_argument("");
    }

    i++;
    emplace_back(FuzzySetElem(str.substr(0, i)));

    if (i >= str.length()) {
      break;
    }

    str = str.substr(i + 1);
  }
}

std::string FuzzySet::toString() const {
  std::string str = "{";

  for (const auto &el : *this) {
    str += el.toString() + ",";
  }

  if (str.size() > 1) {
    str.pop_back();
  }

  str += "}";

  if (!name.toString().empty()) {
    str.insert(0, name.toString() + "=");
  }

  return str;
}

const SetName &FuzzySet::getName() const {
  return name;
}

Relation::Relation(const std::string &inStr) {
  std::istringstream inStrStream(inStr);

  {
    std::string line;
    std::getline(inStrStream, line);

    if (const size_t i = line.find("=("); i > 1) {
      throw std::invalid_argument("");
    }

    name = RelationName(line.substr(0, 1));
  }

  std::string line;
  while (std::getline(inStrStream, line)) {
    if (line == ")") {
      return;
    }

    matrix.push_back({});

    std::istringstream lineStream(line);
    double val = 0;
    while (lineStream >> val) {
      matrix.back().push_back(val);
    }
  }

  throw std::invalid_argument("");
}

const RelationMatrix &Relation::getMatrix() const {
  return matrix;
}

const RelationName &Relation::getName() const {
  return name;
}

ReverseConclusion::ReverseConclusion(std::string str) {
  {
    const size_t i = str.find('=');
    if (i == std::string::npos) {
      throw std::invalid_argument("");
    }

    ySetName = SetName(str.substr(i + 1));
    str = str.substr(0, i);
  }

  if (str.front() != '{' || str.back() != '}') {
    throw std::invalid_argument("");
  }

  str = str.substr(1);
  str.pop_back();

  {
    const size_t i = str.find(',');
    if (i == std::string::npos) {
      throw std::invalid_argument("");
    }

    xSetName = SetName(str.substr(0, i));
    relName = RelationName(str.substr(i + 1));
  }
}

std::string ReverseConclusion::toString() const {
  std::string res = "";

  if (sols.empty()) {
    return res + "∅";
  }

  res += "⟨";

  for (size_t i = 0; i < sols.front().size(); i++) {
    res += xSetName.toString() + "(x" + std::to_string(i + 1) + "),";
  }

  res.pop_back();
  res += "⟩∈";

  for (const auto &sol : sols) {
    res += "(";

    for (const auto &range : sol) {
      std::string rangeStr = doubleToString(range.first);

      if (range.first != range.second) {
        rangeStr += "," + doubleToString(range.second);
      }

      res += "[" + rangeStr + "]×";
    }

    res = res.substr(0, res.size() - std::string("×").size());
    res += ")∪";
  }

  res = res.substr(0, res.size() - std::string("∪").size());

  return res;
}

void ReverseConclusion::setSolutions(Solutions inSols) {
  sols = std::move(inSols);
}

const SetName &ReverseConclusion::getXSetName() const {
  return xSetName;
}

const SetName &ReverseConclusion::getYSetName() const {
  return ySetName;
}

const RelationName &ReverseConclusion::getRelationName() const {
  return relName;
}

std::string ReverseConclusion::doubleToString(double val) {
  std::string res = std::to_string(val);

  while (res.back() == '0') {
    res.pop_back();
  }

  if (res.back() == '.') {
    res += "0";
  }

  return res;
}
