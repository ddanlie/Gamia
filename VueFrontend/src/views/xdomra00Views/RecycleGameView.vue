
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
            <template  v-if="this.currentGame.stage == 0">
                <div class="full two-fifth-1500 textCenter infoWrap">
                    <h1 class="greenColor" style="padding:0;">{{this.currentGame.name}}</h1>
                    <img :src="gameDescriptionSrc" style='max-height: 100vh; max-width: 100%; width: 800px; height: 500px; object-fit: contain' :style="{ opacity: gameDescriptionSrc==='' ? '1' : '1'}">
                </div>
    
                <!-- code -->
                <div class="full half-1000 fifth-1500 textCenter partyCodeWrap">
                    <PartyCodeComponent :code="currentGame.party_code" />
                    <ReadyButtonComponent class="full off-third-500 third-500 off-sixth-1000 two-third-1000" :ready="this.playerIsReady" @readyPressed="this.setReady()"/>
                </div>
            </template>

            <template v-if="this.currentGame.stage == 1">
                <div class="full off-none-1000 half-1000 three-fifth-1500 textCenter promptStageWrap">
                    <h1 class="greenColor" style="padding:0; margin-bottom: 2%;">{{this.currentGame.name}}</h1>
                    <TimeoutWritingComponent class="full off-fourth-500 half-500 off-third-1500 third-1500" :timeToWait="this.currentGame.logic.secTimer"/>
                    <ReadyButtonComponent style="margin-top: 5%;" :ready="this.playerIsReady" @readyPressed="this.setReady()"/>
                </div>
                <!-- "full off-third-1000 third-1000" -->
                <!-- class="off-two-fifth-1500 fifth-1500"  -->
            </template>

            <!-- chat -->
            <div class="full off-fourth-500 half-500 off-none-1000 off-none-1500 fifth-1500 chatWrap">
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
    import ReadyButtonComponent from '../../components/xdomra00Comps/ReadyButtonComponent.vue';
    import TimeoutWritingComponent from '../../components/xdomra00Comps/TimeoutWritingComponent.vue';

    export default {


        beforeDestroy() 
        {
            for(timeout in this.timeouts)
                clearTimeout(timeout);
        },

        components: {
            PartyCodeComponent: PartyCodeComponent, 
            PartyUsersComponent: PartyUsersComponent, 
            ChatComponent: ChatComponent,
            ReadyButtonComponent: ReadyButtonComponent,
            TimeoutWritingComponent: TimeoutWritingComponent
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
                playerIsReady: undefined,
                mounted: undefined
            }   
        },

        watch: {
            currentGame(newInfo, oldInfo)
            {
                if(newInfo.all_ready)
                {
                    this.$api.post("set_next_stage", {
                        gameId: this.currentGame.id,
                        timeout: 1000
                    }, {
                        withCredentials: true
                    })
                    .then(response => {
                        
                    })
                    .catch(error => {
                        this.errorWarning = "Game error";
                        setTimeout(()=>{this.errorWarning=""}, 3000);
                    })
                }
            }
        },

        computed: {
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

                    for(let player of this.currentPlayers)
                    {
                        if(this.user.id == player.id)
                        {
                            this.playerIsReady = player.ready_for_game;
                            break;
                        }
                    }
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
                    setTimeout(() => this.currentGamePoll(currentGameId), 1000);
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
                        userId: this.user.id,
                    }
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

.promptStageWrap
{
    margin-left: 13%;
    min-height: 650px;
}



@media(max-width:1500px)
{
    .infoWrap, .promptStageWrap
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