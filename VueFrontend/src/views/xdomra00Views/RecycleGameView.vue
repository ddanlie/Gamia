
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
                    <ReadyButtonComponent
                        class="full off-third-500 third-500 off-sixth-1000 two-third-1000"
                        :ready="this.playerIsReady"
                        @readyPressed="this.setReady()"/>
                </div>
            </template>

            <template v-if="this.currentGame.stage == 1">
                <div class="full off-none-1000 half-1000 three-fifth-1500 textCenter promptStageWrap">
                    <h1 class="greenColor" style="padding:0; margin-bottom: 2%;">{{this.currentGame.name}}</h1>
                    <TimeoutWritingComponent
                        :newTimer="this.newTimer"
                        @timerSet="this.newTimer = false"
                        @timeOut="this.setReady()"
                        @promptReady="(p) => {this.prompt = p;}"
                        :secondsToWait="this.currentGame.logic.secTimer" 
                        class="full off-fourth-500 half-500 off-third-1500 third-1500"/>
                    <ReadyButtonComponent  
                        @readyPressed="this.setReady()"  
                        :ready="this.playerIsReady"
                        style="margin-top: 5%;"/>
                </div>
            </template>


            <template v-if="this.currentGame.stage >= 2 && this.currentGame.state=='Playing'" :key="this.currentGame.stage" >
                <div class="full fifth-1500 textCenter imgWrap">
                    <img :src="this.describedImgSrc" 
                        style='max-height: 100vh; max-width: 100%; width: 400px; height: 400px; 
                        object-fit: contain' :style="{ opacity: describedImgSrc==='' ? '1' : '1'}">
                </div>
                <div class="full off-none-1000 half-1000 two-fifth-1500 textCenter"
                    style="margin-left: 0%;">
                    <h1 class="greenColor" style="padding:0; margin-bottom: 2%;">{{this.currentGame.name}}</h1>
                    <TimeoutWritingComponent :key="currentGame.stage"
                        :newTimer="this.newTimer"
                        @timerSet="this.newTimer = false"
                        textVal="Describe image!"
                        @timeOut="this.setReady()"
                        @promptReady="(p) => {this.prompt = p;}"
                        :secondsToWait="this.currentGame.logic.secTimer" 
                        class="full off-fourth-500 half-500 off-fourth-1500 half-1500"/>
                    <ReadyButtonComponent 
                        :key="this.currentGame.stage"
                        @readyPressed="this.setReady()"  
                        :ready="this.playerIsReady"
                        style="margin-top: 5%;"/>
                </div>
            </template>


            <template v-if="this.currentGame.state == 'Finished'">
                <div class="full half-1000 three-fifth-1500 resultsWrap">
                    <RecycleResultsComponent class="off-sixth" :gameId="this.currentGame.id"/>
                </div>
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
    import RecycleResultsComponent from '../../components/xdomra00Comps/RecycleResultsComponent.vue';

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
            TimeoutWritingComponent: TimeoutWritingComponent,
            RecycleResultsComponent: RecycleResultsComponent,
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
                errorWarning: "",
                playerIsReady: undefined,
                prompt: "",
                describedImgSrc: "",
                mounted: undefined,
                newTimer: true,
                minStages: 2,
                maxStages: 5//min - 2
            }   
        },

        watch: {
            newTimer(newinfo)
            {
                console.log("TIMER "+newinfo);
            }, 

            'currentGame.stage'(newInfo, oldInfo)
            {
                let newT = false;
                let finish = false;

                if(newInfo >= this.maxStages-1)//last stage - results
                    finish = true;

                if(finish && newInfo > this.maxStages-1)
                    this.currentGame.stage = oldInfo;

                //stage 1 - preparation
                //stage 2 - prompts
                //stage 3 - describe prompts (cycled) 
                if(oldInfo && (newInfo != oldInfo))//description stages
                {
                    newT = true;
                    console.log("NEW STAGE "+newInfo+" OLD "+oldInfo+" Finish: "+finish);
                    if(newInfo >= this.minStages && this.currentGame.state != 'Finished')
                            this.submitPrompt(!finish);
                }
                if(!oldInfo && !this.newTimer)
                    newT = true;

                if(finish)
                    this.finishGame()

                this.newTimer = newT;
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
                    this.currentGame.logic = JSON.parse(this.currentGame.logic);
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
                    this.currentGame.logic = JSON.parse(this.currentGame.logic);
                    console.log("3. Current game = "+JSON.stringify(this.currentGame));
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
            },


            submitPrompt(getNextPicture=true)
            {
                this.$api.post("recycle_submit_prompt", {
                    userId: this.user.id,
                    prompt: this.prompt,
                }, {
                    withCredentials: true,
                    timeout: 10000
                })
                .then(response => {
                    if(getNextPicture)
                        this.getPictureToDescribe();
                })
                .catch(error => {
                    this.errorWarning = "Submit error";
                    setTimeout(()=>{this.errorWarning=""}, 3000);
                })
            },

            getPictureToDescribe()
            {
                this.$api.get("recycle_prepare_describing", {
                    params: {
                        userId: this.user.id,
                    },
                    timeout: 10000
                })
                .then(response => {
                    this.describedImgSrc = response.data.src; 
                })
                .catch(error => {
                    this.errorWarning = "Error, could not get image";
                    setTimeout(()=>{this.errorWarning=""}, 3000);
                })
            },

            finishGame()
            {
                if(!this.mounted)
                    return;

                this.$api.post("finish_game", {
                    id: this.currentGame.id
                }, {
                    withCredentials: true
                })
                .catch(error => {
                    setTimeout(this.finishGame, 300);
                })
            },
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

.imgWrap
{
    margin-left:13%; 
    margin-top: 5%;
}

.resultsWrap
{
    margin-left:13%; 
}


@media(max-width:1500px)
{
    .infoWrap, .promptStageWrap, .imgWrap, .resultsWrap
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