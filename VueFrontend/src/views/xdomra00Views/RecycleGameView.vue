
<template>

    <div class="flex one center">
        <!-- game table -->
        <div class="flex five">
            <!-- main content -->
            <div class="flex four four-fifth">
                <div class="full">
                    <button class="redBack blackColor" style="margin: 2% 0 0 2%;  padding: 1% 2% 1% 2%">Quit</button>
                </div>

                <div class="three-fourth textCenter">
                    <h1 style="padding:0;">Recycle</h1>
                    <img :src="gameDescriptionSrc" style='max-height: 100vh; max-width: 100%; width: 800px; height: 500px; object-fit: contain' :style="{ opacity: gameDescriptionSrc==='' ? '1' : '1'}">
                </div>

                <div class="fourth textCenter">
                    <PartyCodeComponent/>
                </div>
            </div>

            <!-- chat -->
            <div class="fifth">
                <ChatComponent/>
            </div>
        </div>
        
        <!-- players -->
        <div class="flex">
            <PartyUsersComponent :users="currentPlayers"/>
        </div>
    </div>

</template>


<script>
    import PartyCodeComponent from '../../components/xdomra00Comps/PartyCodeComponent.vue';
    import PartyUsersComponent from '../../components/xdomra00Comps/PartyUsersComponent.vue';
    import ChatComponent from '../../components/xivano08Comps/ChatComponent.vue';

    export default {

        components: {
            PartyCodeComponent: PartyCodeComponent, 
            PartyUsersComponent: PartyUsersComponent, 
            ChatComponent: ChatComponent
        },

        mounted() 
        {
            this.setUserThenGame();
        },

        data() 
        {
            return {
                gameDescriptionSrc: "",
                currentGame: "",
                user: "",
                currentPlayers: "",
                errorWarning: ""
            }   
        },

        methods: {

            setUserThenGame()
            {
                this.$api.get("fantom_user")
                .then(response => {
                    this.user = response.data;
                    console.log("1. Current user = "+JSON.stringify(this.user));

                    this.setPLayedGame(this.user.current_game_id);
                })
                .catch(error => {
                    setTimeout(this.setFantomUser, 2000);
                    // console.log(error);
                })
            },
            
            setPLayedGame(currentGameId)
            {
                this.$api.get("played_game", {
                    params: {
                        id: currentGameId
                    }
                })
                .then(response => {
                    this.currentGame = response.data;
                    console.log("2. Current game = "+JSON.stringify(this.currentGame));

                    this.setGameInfo(this.currentGame.game_id);
                    this.currentPlayersPoll(currentGameId);
                })
                .catch(error => {
                    setTimeout(() => this.setPLayedGame(currentGameId), 2000);
                    // console.log(error);
                })
            },

            setGameInfo(gameId)
            {
                this.$api.get("game_info", {
                    params: {
                        id: gameId
                    }
                })
                .then(response => {
                    this.gameDescriptionSrc = response.data.src;

                })
                .catch(error => {
                    setTimeout(setGame, 2000);
                    // console.log(error);
                })
            },

            currentPlayersPoll(currentGameId)
            {
                this.$api.get("game_players", {
                    params: {
                        id: currentGameId
                    }
                })
                .then(response => {
                    this.currentPlayers = response.data;
                    setTimeout(() => this.currentPlayersPoll(currentGameId), 5000);
                })
                .catch(error => {
                    setTimeout(() => this.currentPlayersPoll(currentGameId), 2000);
                    // console.log(error);
                })
            }
        }
    }

</script>