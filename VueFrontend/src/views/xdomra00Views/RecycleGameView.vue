
<template>
    <div v-if="this.currentGame" class="flex one center">
        <h4 v-if="errorWarning" class="redColor">
            {{ errorWarning }}
        </h4>
        <!-- game table -->
        <div class="flex five">
            
            <div class="full">
                <button @click="this.disconnectUser" class="redBack" style="margin: 2% 0 0 2%;  padding: 1% 2% 1% 2%">
                    <h3 class="blackColor zeroPad">
                        Quit
                    </h3>
                </button>

            </div>

            <!-- main content -->
            <div class="full two-fifth-1500 textCenter infoWrap">
                <h1 class="greenColor" style="padding:0;">{{this.currentGame.name}}</h1>
                <img :src="gameDescriptionSrc" style='max-height: 100vh; max-width: 100%; width: 800px; height: 500px; object-fit: contain' :style="{ opacity: gameDescriptionSrc==='' ? '1' : '1'}">
            </div>

            <!-- code -->
            <div class="full half-500 fifth-1500 textCenter partyCodeWrap">
                <PartyCodeComponent :code="currentGame.party_code" :ready="this.playerIsReady" @readyPressed="this.setReady()"/>
            </div>

            <!-- chat -->
            <div class="full half-500 off-none-1500 fifth-1500 chatWrap">
                <ChatComponent/>
            </div>
            <!-- players -->
            <div class="full partyUsersWrap">
                <PartyUsersComponent :users="currentPlayers"/>
            </div>
        </div>
        


    </div>
</template>


<script>
    import PartyCodeComponent from '../../components/xdomra00Comps/PartyCodeComponent.vue';
    import PartyUsersComponent from '../../components/xdomra00Comps/PartyUsersComponent.vue';
    import ChatComponent from '../../components/xivano08Comps/ChatComponent.vue';

    export default {


        beforeDestroy() 
        {
            for(timeout in this.timeouts)
                clearTimeout(timeout);
        },

        components: {
            PartyCodeComponent: PartyCodeComponent, 
            PartyUsersComponent: PartyUsersComponent, 
            ChatComponent: ChatComponent
        },

        mounted() 
        {
            this.mounted = true;
            this.setUserThenGame();
        },

        unmounted()
        {
            this.mounted = false;
        },

        data() 
        {
            return {
                gameDescriptionSrc: "",
                currentGame: "",
                user: "",
                currentPlayers: "",
                currentGame: "",
                errorWarning: "",
                playerIsReady: false,
                mounted: undefined
            }   
        },

        methods: {

            setUserThenGame()
            {
                if(!this.mounted)
                    return;
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
                if(!this.mounted)
                    return;

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
                    this.currentGamePoll(currentGameId);
                })
                .catch(error => {
                    setTimeout(() => this.setPLayedGame(currentGameId), 2000);
                    // console.log(error);
                })
            },

            setGameInfo(gameId)
            {
                if(!this.mounted)
                    return;
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
                if(!this.mounted)
                    return;

                this.$api.get("game_players", {
                    params: {
                        id: currentGameId
                    }
                })
                .then(response => {
                    this.currentPlayers = response.data;
                })
                .catch(error => {
                    // console.log(error);
                })
                .finally(() => {
                    setTimeout(() => this.currentPlayersPoll(currentGameId), 2000);
                })
            },

            currentGamePoll(currentGameId)
            {
                if(!this.mounted)
                    return;

                this.$api.get("played_game", {
                    params: {
                        id: currentGameId
                    }
                })
                .then(response => {
                    this.currentGame = response.data;
                })
                .catch(error => {
                    // console.log(error);
                })
                .finally(() => {
                    setTimeout(() => this.currentGamePoll(currentGameId), 2000);
                })
            },

            disconnectUser()
            {
                this.$api.post("disconnect_player", {
                    id: this.user.id
                }, {
                        withCredentials: true
                })
                .then(response => {
                    this.$router.push({ name: "home" });
                })
                .catch(error => {
                    this.errorWarning = "Error, cant't disconnect";
                    setTimeout(()=>{this.errorWarning=""}, 3000);
                })
            },

            setReady()
            {
                this.$api.get("toggle_ready", {
                    params: {
                        userId: this.user.id
                    }
                })
                .then(response => {
                    this.playerIsReady = response.data.ready;
                })
                .catch(error => {
                    this.errorWarning = "Error";
                    setTimeout(()=>{this.errorWarning=""}, 3000);
                })
            }
        }
    }

</script>


<style scoped>

.infoWrap
{
    margin-left: 13%;
    min-height: 650px;
}

@media(max-width:1500px)
{
    .infoWrap
    {
        margin-left: 0;
    }
}

.partyUsersWrap
{
    margin: 2% 0% 0% 1%;
    padding: 0% 2% 0% 2%;
}

.chatWrap
{
    min-height: 650px;
}

@media(max-width:1500px)
{
    .chatWrap
    {
        min-height: 800px;
    }
}

.partyCodeWrap
{
    margin: 8% 0% 0 0%;
    padding: 0;
    
}

</style>