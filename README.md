# BEST_GPGPU_filter
## Rozwiązanie zadania

### Instsrukcja programisty
Filtr obsługuje klasa RegFilter. Po zainicjalizowaniu obiektu
należy wywołać metodę bake_regex z parametrem listy wulgaryzmów.
Gdy istnieje już plik baked.txt filtr można ładować metodą load_regex.
Do analizy frazy służy metoda check_phrase
```python
# przykład użycia filtra
if __name__ == '__main__':
    my_filter = RegFilter().bake_regex(wulgaryzmy)
    phrase = 'Twoja stara to chuj i zaje#b1śCi3, cchuuuj, kurwi#ska, cuhj, kurvviszonem, cip@, spierdaia, jebal'
    print(phrase)
    print(my_filter.check_phrase(phrase))
```

### Opis rozwiązania
W naszym rozwiązaniu zastosowaliśmy wyrażenia regularne 
do odnajdywania słów wulgarnych. Do stworzenia jednego długiego
wyrażenia używane są pomniejsze (regex tworzy regex). Dzięki zastosowaniu 
struktury drzewiastej TRIE rozwiązanie skaluje się bardzo dobrze do dużej
ilości słów jak również w znacznym stopniu przyspiesza działanie.

1. Wulgaryzmy zaczerpnięte z otwartej bazy https://marcinmazurek.com.pl/polskie-wulgaryzmy
   (baza uwzględania odmiany słów), słowa są znajdowane przez długi drzewiasty Regex
2. zamiana znaków (i,e,a,o,u) na kolejno: (1,3,4,0,v)
-  każda litera w słowie jest zastępowana przez regex uwzględniający możliwość zamiany znaków
3. powtarzanie niektórych liter w danym wyrazie, np. “ssłoowo”, litera "w" zamieniona na "vv"
-  wyrażenie regex zakłada ża każda litera w słowie może powtórzyć się nieskończenie pod rząd
4. słowa mogą występować z różnymi końcówkami fleksyjnymi:
- uwzględnione przez bazę danych
5. próby obejścia filtra poprzez dostawienie do wyrazu losowego znaku (na przykład spacji)
- po każdej literze może wystąpić znak specjalny
6.  zamiana kolejności dwóch liter
- każde słowo z bazy jest powielane i modyfikowane tak by wystąpiły wszystkie możliwe wersje
zamiany kolejności, potencjalna nieoptymalność rozwiązania jest kompensowana w całości przez zastosowanie drzewiastej struktury TRIE
