<?php

    require_once("Game.php");
    require_once("Deck.php");

	$numGames = 100000;
    $results = array();
    $winningStates = array();

    for($i = 0; $i<$numGames; ++$i)
    {
        if($i%10000==0)
        {
            echo "$i...";
        }
        $d = new Deck();
        $d->shuffle();
        $g = new Game($d);
        $turns = $g->play();
        $results[] = $turns;
        if($turns ==1){echo "YOU WON!\n";$winningStates[]=$g->boardToString();}
    }
    echo "Final results:\n";
    foreach($results as $result)
    {
        echo "$result,";
    }
    echo "\n";
    echo "Average: ".(array_sum($results)/count($results))."\n";
    var_dump($winningStates);



?>
