
<template>
    <div class="flex one">
        <h1 class="full greenColor">Welcome to <span class="redColor">Gamia</span></h1>
        <div class="flex three textCenter">
            <!-- left block -->
            <div class="flex center full half-1000 third-1500">
                <div class="full">
                    <h2 class="redColor">Games</h2>
                    <ul class="menuUl">
                        <li v-for="game in allGames" :key="game.id" >
                            <button @mouseover="getGameDescription(game.id)" @mouseleave="emptyGameDescription()" class="fourth redColor menuButton" style="font-size: 24px;">{{ game.name }}</button>
                        </li>

                    </ul>
                </div>
                <form  @submit.prevent="handleJoin" class="flex one center">
                    <div class="center third">
                        <h2 class="redColor"> Connect</h2>
                        <div class="spanPad">
                            <input class="two-third" type="text">
                            <button class="third" @click="" style="color: #F2FF00; background-color: #52D6B5;">Join</button>
                        </div>
                    </div>
                </form>
            </div>
            <!-- right block  -->
            <div class="flex center full half-1000 two-third-1500 ">
                <img class="flex" :src="gameDescriptionSrc" style='max-height: 100vh; max-width: 100%; width: auto; height: auto; object-fit: contain' :style="{ opacity: gameDescriptionSrc==='' ? '0' : '1'}">
            </div>
        </div>
    </div>
          <!-- <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav> -->


  <!-- <RouterView /> -->

</template>


<script>

    export default {

        mounted() {

            const getAllGames = () => {
                this.$api.get("all_games")
                .then(response => {
                    this.allGames = response.data;
                    console.log("got it")
                })
                .catch(error => {
                    setTimeout(getAllGames, 2000);
                    console.log(error)
                })
            }

            getAllGames();
        },

        data() {
            return {
                allGames: "",
                gameDescriptionSrc: "",
                menuGameId: ""
            }   
        },

        methods: {
            handleJoin()
            {

            },

            getGameDescription(gameId)
            {   
                this.menuGameId = gameId;

                this.$api.get("game_info", {
                        params: {
                            "id": gameId
                        }
                })
                .then(response => {
                    this.gameDescriptionSrc = response.data.src;
                })
                .catch(error => {
                    setTimeout(getAllGames, 2000);
                    console.log(error)
                })
            },

            emptyGameDescription()
            {
                this.menuGameId = "";
                this.gameDescriptionSrc = ""
            }
        }

    }
</script>



<style scoped>

.menuUl
{ 
    max-height: 300px; 
    overflow-y:auto;
    scrollbar-width: thin; /* Make scrollbar thin */
    scrollbar-color: #52D6B5 #FCEEDF; /* Change scrollbar thumb and track colors */
}

.spanPad
{
    border-radius: 15px;
    padding: 5px 10px 5px 10px;
    background-color: #52D6B5;
}


.greenColor
{
    color:#52D6B5
}

.redColor
{
    color:#F97D7B
}

.menuButton
{

    background-color: rgba(251, 190, 91, 0.14);
    padding: 2% 0 2% 0
}

.menuButton:hover
{
    transition: 0s;
    outline: solid;
    outline-color:#52D6B5;
    
}

.textCenter
{
    text-align: center;
} 

h1 
{
    font-family: "Jua", cursive;
    font-size: 64px;

}

h2 
{
    font-family: "Jua", cursive;
    font-size: 48px;

}


</style>

