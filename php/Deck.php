<?php

    abstract class Suit
    {
        const Spades = 0;
        const Hearts = 1;
        const Diamonds = 2;
        const Clubs = 3;
    }
    abstract class Rank
    {
        const Two = 2;
        const Three = 3;
        const Four = 4;
        const Five = 5;
        const Six = 6;
        const Seven = 7;
        const Eight = 8;
        const Nine = 9;
        const Ten = 10;
        const Jack = 11;
        const Queen = 12;
        const King = 13;
        const Ace = 14;
    }

    class Card
    {
        public $rank;
        public $suit;

        public function __construct($rank, $suit)
        {
            $this->rank = $rank;
            $this->suit = $suit;
        }
        public function toString()
        {
            $toReturn = "";
            switch($this->rank)
            {
                case 2:
                    $toReturn .= "Two";
                    break;
                    case 3:
                    $toReturn .= "Three";
                    break;
                    case 4:
                    $toReturn .= "Four";
                    break;
                    case 5:
                    $toReturn .= "Five";
                    break;
                    case 6:
                    $toReturn .= "Six";
                    break;
                    case 7:
                    $toReturn .= "Seven";
                    break;
                    case 8:
                    $toReturn .= "Eight";
                    break;
                    case 9:
                    $toReturn .= "Nine";
                    break;
                    case 10:
                    $toReturn .= "Ten";
                    break;
                    case 11:
                    $toReturn .= "Jack";
                    break;
                    case 12:
                    $toReturn .= "Queen";
                    break;
                    case 13:
                    $toReturn .= "King";
                    break;
                    case 14:
                    $toReturn .= "Ace";
                    break;
            }
            switch ($this->suit)
            {
                case 0:
                    $toReturn .= " of Spades";
                    break;
                case 1:
                    $toReturn .= " of Hearts";
                    break;
                case 2:
                    $toReturn .= " of Diamonds";
                    break;
                case 3:
                    $toReturn .= " of Clubs";
                    break;
            }
            return $toReturn;
        }
        public function toShortString()
        {
            $toReturn = "";
            switch($this->rank)
            {
                case 2:
                    $toReturn .= "2";
                    break;
                    case 3:
                    $toReturn .= "3";
                    break;
                    case 4:
                    $toReturn .= "4";
                    break;
                    case 5:
                    $toReturn .= "5";
                    break;
                    case 6:
                    $toReturn .= "6";
                    break;
                    case 7:
                    $toReturn .= "7";
                    break;
                    case 8:
                    $toReturn .= "8";
                    break;
                    case 9:
                    $toReturn .= "9";
                    break;
                    case 10:
                    $toReturn .= "10";
                    break;
                    case 11:
                    $toReturn .= "J";
                    break;
                    case 12:
                    $toReturn .= "Q";
                    break;
                    case 13:
                    $toReturn .= "K";
                    break;
                    case 14:
                    $toReturn .= "A";
                    break;
            }
            switch ($this->suit)
            {
                case 0:
                    $toReturn .= "s";
                    break;
                case 1:
                    $toReturn .= "h";
                    break;
                case 2:
                    $toReturn .= "d";
                    break;
                case 3:
                    $toReturn .= "c";
                    break;
            }
            return $toReturn;
        }
    }

    class Deck
    {
        public $_deck;

        public function __construct()
        {
            $this->_deck = array();
            for($i = 0; $i<=3; ++$i) {
                for($j = 2; $j<=14; ++$j)
                {
                    $this->_deck[] = new Card($j, $i);
                }
            }
        }
        public function shuffle()
        {
            shuffle($this->_deck);
        }
        public function printDeck()
        {
            foreach ($this->_deck as $card)
            {
                echo $card->toShortString()." | ";
            }
        }
        public function getCard()
        {
            return array_shift($this->_deck);
        }
    }


?>