
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
                            <button type="submit" for="createGameForm" @click="createNewGame()" @mouseover="setGameInfo(game.id)" @mouseleave="emptyGameDescription()" class="fourth redColor menuButton" style="font-size: 24px;">{{ game.name }}</button>
                        </li>
                    </ul>
                    <h3 v-if="errorWarning != ''" style="color:red;">{{ errorWarning }}</h3>
                    <form id="createGameForm" @submit.prevent style="margin-top: 5%;">
                        <label>
                            <input type="checkbox" v-model="privateFlag">
                            <span class="checkable">Private game</span>
                        </label>
                    </form>
                </div>
                <form  @submit.prevent="handleJoin" class="flex one center">
                    <div class="center third">
                        <h2 class="redColor">Connect</h2>
                        <div class="spanPad">
                            <input class="two-third" type="text" v-model="partyCode">
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

        mounted() 
        {
            this.setFantomUser();
            this.getAllGames();

            
        },

        data() 
        {
            return {
                allGames: "",
                gameDescriptionSrc: "",
                gameRouteName: "",
                chosenGameId: "",
                user: "",
                privateFlag: false,
                partyCode: "",
                errorWarning: "",
            }   
        },

        methods: {
            handleJoin()
            {

            },

            setFantomUser()
            {
                this.$api.get("fantom_user")
                .then(response => {
                    this.user = response.data;
                    console.log("Current user = "+this.user['name']);
                })
                .catch(error => {
                    setTimeout(this.setFantomUser, 2000);
                    // console.log(error);
                })
            },

            getAllGames()
            {
                this.$api.get("all_games")
                .then(response => {
                    this.allGames = response.data;
                    console.log("got all games");
                })
                .catch(error => {
                    setTimeout(this.getAllGames, 2000);
                    // console.log(error);
                })
            },

            setGameInfo(gameId)
            {   
                this.chosenGameId = gameId;

                this.$api.get("game_info", {
                    params: {
                        id: gameId
                    }
                })
                .then(response => {
                    this.gameDescriptionSrc = response.data.src;
                    this.gameRouteName = response.data.routeName;
                })
                .catch(error => {
                    setTimeout(() => this.setGameInfo(gameId), 2000);
                    // console.log(error)
                })
            },

            emptyGameDescription()
            {
                this.chosenGameId = "";
                this.gameDescriptionSrc = ""
            },

            createNewGame()
            {
                this.$api.post("create_game_for", {
                        userId: this.user.id,
                        gameId: this.chosenGameId,
                        private: this.privateFlag
                }, {
                        withCredentials: true
                })
                .then(response => {
                    this.$router.push({ name: this.gameRouteName });
                })
                .catch(error => {
                    this.errorWarning = "Error, try again";
                    setTimeout(()=>{this.errorWarning=""}, 3000);
                })
            }
        }

    }
</script>



<style scoped>

.menuUl
{ 
    max-height: 200px; 
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

h3 
{
    font-family: "Jua", cursive;
    font-size: 12px;
}


</style>

