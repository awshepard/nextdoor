<?php

    require_once("Deck.php");

    class Game
    {

        public $board;
        public $deck;
        public $lastIndex;
        public $strategy;

        public function __construct($deck, $strategy = "naive")
        {
            $this->board = array();
            $this->board[0] = array();
            $this->deck = $deck;
            $this->lastIndex = -1;
            $this->strategy = $strategy;
        }

        public function play()
        {
            $count = 1;
            //echo "Starting Game:\n";
            //$this->printBoard();
            while(($card = $this->deck->getCard()) !== null)
            {
                switch($this->strategy)
                {
                    case "dad":

                        break;
                    case "naive":
                    default:
                        $this->turn($card);
                        break;
                }
                //echo "After Turn $count:\n";
                //$this->printBoard();
                //pause
                //$line = fgets(STDIN);
                //echo "Running collapse:\n";
                switch($this->strategy)
                {
                    case "dad":

                        break;
                    case "naive":
                    default:
                        $this->collapse();
                        break;
                }

                //echo "After collapse:\n";
                //$this->printBoard();
                //pause
                //$line = fgets(STDIN);
                $count++;
            }
            //$this->printBoard();
            return count($this->board);
        }

        public function turn($card)
        {
            //var_dump($this->board[$this->lastIndex][0]->rank);
            //decide where to put card
            if($this->lastIndex>-1 && (
                $this->board[$this->lastIndex][0]->rank == $card->rank ||
                $this->board[$this->lastIndex][0]->suit == $card->suit))
            {
                //put card at top of next door pile
                array_unshift($this->board[$this->lastIndex],$card);
            }
            else if($this->lastIndex>=2 && ($this->board[$this->lastIndex-2][0]->rank == $card->rank || $this->board[$this->lastIndex-2][0]->suit == $card->suit))
            {
                    //put card at top of skip two pile
                array_unshift($this->board[$this->lastIndex-2],$card);
            }
            else
            {
                //put card in new pile
                $this->lastIndex += 1;
                $this->board[$this->lastIndex] = array();
                array_unshift($this->board[$this->lastIndex],$card);
            }
            //collapse board
            //echo "collapsing...\n";
            //$this->collapse();
        }
        public function turnDad($card)
        {
                        //var_dump($this->board[$this->lastIndex][0]->rank);
            //decide where to put card
            if($this->lastIndex>-1 && (
                $this->board[$this->lastIndex][0]->rank == $card->rank ||
                $this->board[$this->lastIndex][0]->suit == $card->suit))
            {
                //put card at top of next door pile
                array_unshift($this->board[$this->lastIndex],$card);
            }
            else if($this->lastIndex>=2 && ($this->board[$this->lastIndex-2][0]->rank == $card->rank || $this->board[$this->lastIndex-2][0]->suit == $card->suit))
            {
                    //put card at top of skip two pile
                array_unshift($this->board[$this->lastIndex-2],$card);
            }
            else
            {
                //put card in new pile
                $this->lastIndex += 1;
                $this->board[$this->lastIndex] = array();
                array_unshift($this->board[$this->lastIndex],$card);
            }
            //collapse board
            //echo "collapsing...\n";
            //$this->collapse();
        }

        public function collapse()
        {
            do
            {
                $movedCards = false;
                for($i = 1; $i<=$this->lastIndex; $i++)
                {
                    //check to see if i can move this up the chain
                    if($i>=1)
                    {
                        //echo "last Index is {$this->lastIndex}\n";
                        //echo "Checking ".$this->board[$i-1][0]->toShortString()." vs. ".$this->board[$i][0]->toShortString()."\n";
                        if($this->board[$i-1][0]->rank == $this->board[$i][0]->rank ||
                           $this->board[$i-1][0]->suit == $this->board[$i][0]->suit )
                        {
                            //echo "Moving next door!\n";
                            //do move
                            $this->board[$i-1] = array_merge($this->board[$i],$this->board[$i-1]);
                            array_splice($this->board,$i,1);
                            $this->lastIndex--;
                            //set movedcards
                            $movedCards = true;
                            break;
                        }
                    }
                    if ($i >= 3)
                    {
                        //echo "Checking ".$this->board[$i-3][0]->toShortString()." vs. ".$this->board[$i][0]->toShortString()."\n";
                        if($this->board[$i-3][0]->rank == $this->board[$i][0]->rank ||
                           $this->board[$i-3][0]->suit == $this->board[$i][0]->suit )
                        {
                            //do move
                            //echo "Moving skip two!";
                            $this->board[$i-3] = array_merge($this->board[$i],$this->board[$i-3]);
                            array_splice($this->board,$i,1);
                            $this->lastIndex--;
                            //set movedcards
                            $movedCards = true;
                            break;
                        }

                    }
                }
                //$this->printBoard();
                //$line = fgets(STDIN);
            }while($movedCards);
        }
        public function printBoard()
        {
            foreach($this->board as $pile)
            {
                foreach($pile as $card)
                {
                    echo " | ".$card->toShortString();
                }
                echo "\n";
            }
            //var_dump($this->board);
        }
        public function boardToString()
        {
            $toReturn = "";
            foreach($this->board as $pile)
            {
                foreach($pile as $card)
                {
                    $toReturn .= " | ".$card->toShortString();
                }
                $toReturn .= "\n";
            }
            return $toReturn;
        }

    }




?>