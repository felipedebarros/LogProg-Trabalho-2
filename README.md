#LogProg-Trabalho-2

**Funcionamento do programa**

A entrada do frame é realizada pelo arquivo *frame.json*
Nele temos as seguintes entradas:

 - *states* : Estados presentes no frame, correspondentes aos vértices do grafo correspondente
 - *realstate* : Estado real do sistema
 - *symbols* : O conjunto de símbolos proposicionais, ou átomos, que estão no contexto do frame
 - *relationships* : As relações entre os estados, correspondentes às arestas do grafo. As relações são inclusas em modos diferentes. No exemplo de frame atual, os modos possíveis são a ou b, podendo-se remove-los ou inserir outros da mesma forma. Com base no modelo epistêmico, todo estado deve ter uma relação apontando para ele mesmo.
 - *valuation* : Os conjuntos de estados nos quais cada símbolo é válido.

Para rodar o verificador:
	python valuation.py

O programa vai pedir a entrada da fórmula
	"Formula: "

No formato:
AND- '&'
OR-  '|'
NOT- '~'
IMPLIES- '->' 
a Knows- '[a]'
a Believes- '<a>'
SYMBOLS- Qualquer string alfanumérica

Anúncios são expressos no início da fórmula usando {anúncio}

Por exemplo:

{p}[a]p->q

"Dado que é conhecido publicamente que p é verdadeiro, avalie a fórmula 
[a]p->q"

Anúncios são podas no grafo descrito no arquivo frame.json em que estados onde o anúncio é falso são cortados.

(Devido a limitações no parser, as operações de ~, [] e <> devem seguir a ordem de '~<>[]p', qualquer inversão na ordem desses operadores é necessário o uso de parênteses Ex.: '[](~<>p)' ou '[](<>(~p))' )

Saída
O programa retorna com 'True' ou 'False' segundo o resultado da validação