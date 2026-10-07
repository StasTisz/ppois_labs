/**
* @file adjacent_iterator.h
 * @brief Итераторы смежных вершин для графа.
 * @note Файл предназначен для включения (include) внутрь шаблона Graph<T>.
 */

#pragma once

// ==========================================
// ИТЕРАТОРЫ СМЕЖНЫХ ВЕРШИН
// ==========================================

// Итераторы смежных вершин обязаны быть константными, чтобы пользователь
// не сломал структуру Вирта, перезаписав ключ назначения в обход методов графа.
using adjacent_iterator = typename std::list<T>::const_iterator;
using const_adjacent_iterator = typename std::list<T>::const_iterator;
using reverse_adjacent_iterator = std::reverse_iterator<adjacent_iterator>;
using const_reverse_adjacent_iterator = std::reverse_iterator<const_adjacent_iterator>;