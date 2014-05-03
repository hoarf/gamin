#Sobre este Documento

Este é um relatório sobre a atividade de desenvolvimento de um algoritmo genético para a cadeira de Computação Evolutiva cursada no primeiro semestre de 2014 no Instituto de Informática da Universidade Federal do Rio Grande do Sul (UFRGS).im

#Sobre o algoritmo

## Objetivo

Dada uma função $f=(x,y)$, com $x,y \in [a:b]$ onde $a,b \in \Re$, encontrar um par de pontos $(x_1,y_1) \in [a:b]$ tal que o valor de $f(x_1,y_1)$ seja o menor possível.
    
## Representação

Um _indivíduo_ corresponde a uma coordenada $(x_i,y_i)$ do problema acima e o seu _fenótipo_ é dado pela função de avaliação $f_i=(x_i,y_i)$. Dizemos que indivíduos com menor valor de f são considerados mais adaptados e possuem um fenótipo vantajoso, portanto tem maior chance de ser selecionados. Cada _gene_ do indivíduo é representado por um vetor de 0's e 1's de tamanho arbitrário $R$. Cada valor dentro do gene é chamado de _alelo_.

Um indivíduo é composto por um par de genes que correspondem a cada uma das coordenadas $x$ e $y$. A conversão da cadeia de bits para o seu valor $V \in \Re$ é dada pela seguinte fórmula.

$$V=a+(b-a)*U/2^R-1$$

Onde $U$ corresponde ao valor da cadeia de bits convertido para um número inteiro sem sinal.

## Resumo

O algoritmo segue a seguinte idéia básica

1. O algoritmo inicia a sua execução com uma população inicial de inidivíduos $P$ de tamanho $n$ com genótipos escolhidos aleatoriamente

2. A seguir a roleta é girada $n$ vezes para produzir uma nova população do indivíduos selecionados.

3. Estes indivíduos então são agrupados em pares.

4. Cada par sofre o processo de *crossover* que consiste em:

4.1 Escolher um ponto arbitrário entre $1$ e $R-1$ que servirá de ponto de corte.

4.2 O genótipo do integrante do par é trocado pelo mesmo trecho do outro indivíduo pertecente ao par

5. A seguir cada indivíduo da população depois de sofrer o *crossover* com algum par recebe uma chance $M$ de que cada bit do seu genótipo possa ser invertido.

6. O processo continua volta para o passo 2 até que o algoritmo tenha executado $K$ iterações.

## Método de seleção

O método de seleção utilizado foi a escolha por roleta.

Este método consiste em estabelecer o *pool* de *fitness* $F$ de uma população $P$ de tamanho $n$. Em seguida é avaliada a contribuição de cada indivíduo para o pool: {$f_i | i \in 1..n$}.

Então, a probabilidade de um indivíduo ser escolhido $P_i$ é:

$$P_i = f_i/F$$

Determinadas as probabilidades de seleção de cada indivíduo, uma nova população de tamanho $n$ é sorteada.

## *Crossover*

Dada a representação vetorial dos genes do indivíduo com o primeiro índice do vetor sendo igual a 0, o *crossover* consiste em estipular um ponto de corte aleatório $p \in 1..R-1$. 

Com este ponto, dois novos indivíduos são gerados com os genótipos contendo a troca dos genes naquele ponto.

Exemplo:

Sejam os indivíduos dados em uma representação de tamanho $R = 6$ e um ponto de corte $p_x = 2 $ e $p_y = 3$:

$i_1_x =$ [ <span class="i1">0 1 | 0 0 0 1</span> ] 
$i_2_x =$ [ <span class="i2">1 1 | 0 1 0 0</span> ]


$i_1_y =$ [ <span class="i1">0 0 0 | 1 1 1</span> ] 
$i_2_y =$ [ <span class="i2">0 1 0 | 0 0 1</span> ]

O resultado do *crossover* produzido será:

$i_3_x =$ [ <span class="i2">1 1</span> | <span class="i1"> 0 0 0 1</span> ] 
$i_4_x =$ [ <span class="i1">0 1</span> | <span class="i2"> 0 1 0 0</span> ]

$i_3_y =$ [ <span class="i2">0 1 0</span> | <span class="i1"> 1 1 1</span> ] 
$i_4_y =$ [ <span class="i1">0 0 0</span> | <span class="i2"> 0 0 1</span> ]

## Mutação

Para cada alelo de cada gene do inivíduo resultante do *crossover*, é computada uma chance $M$ do alelo trocar o seu valor, ou seja, os bits que estavam em 1 trocam o seu valor para 0 e vice-versa.

## Resultados Obtidos

Os experimentos abaixo foram executados em uma máquina contendo um processador da família i5 da intel com 4GB de memória RAM.

A linguagem escolhida para a implementação (python) utiliza somente uma thread para a execução do programa.

Todos os valores representam genes com tamanho de representação $R = 20$. Os valores representam a média de 10 execuções

Melhor solução em 10 segundos de execução  Tamanho da população  Taxa de Mutação  
------------------------------------------ --------------------- ----------------
0619.87                                    50                    0.01             
0714.83                                    26                    0.01             
0535.38                                    02                    0.01             
0545.78                                    50                    0.10             
0506.57                                    26                    0.10             
0497.36                                    02                    0.10             
0860.61                                    50                    0.50            
0813.32                                    26                    0.50            
0559.27                                    02                    0.50            

## Conclusão

Os dados coletados sugerem que o aumento do tamnho da população não melhora a performance do algoritmo e pode até piorá-lo para os casos em que a taxa de mutação é muito alta.

Uma taxa de mutação de 10% se mostrou melhor que uma taxa de 1% ou 50%, o que sugere que não há uma correlação linear entre a taxa de mutação e a performance do algoritmo.